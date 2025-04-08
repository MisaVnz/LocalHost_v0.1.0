def validate_request(request):
    """
    Valida una solicitud HTTP según el estándar RFC 2616.
    
    Parámetros:
        request (str): La solicitud HTTP completa como cadena de texto
    
    Retorna:
        dict: {
            "status": int,    # Código de estado HTTP
            "error": str      # Mensaje de error (None si es válida)
        }
    """
    try:
        # Divide el request en líneas usando CRLF (separador estándar HTTP)
        lines = request.split("\r\n")
        
        # --- Validación de la línea de solicitud (request line) ---
        request_line = lines[0].strip()  # Ej: "GET / HTTP/1.1"
        
        # 1. Verifica que la línea no esté vacía
        if not request_line:
            return {
                "status": 400,
                "error": "Bad Request: Empty request line"
            }

        # 2. Divide la línea en 3 partes (método, ruta, versión HTTP)
        parts = request_line.split()
        
        # 3. Verifica que tenga exactamente 3 componentes
        if len(parts) != 3:
            return {
                "status": 400,
                "error": "Bad Request: Malformed request line"
            }
        
        method, path, http_version = parts  # Desempaqueta las partes
        
        # 4. Valida el método HTTP (solo permite los métodos básicos)
        if method not in {"GET", "POST", "PUT", "DELETE"}:
            return {
                "status": 405,
                "error": f"Method Not Allowed: {method}"
            }
        
        # 5. Valida que la ruta comience con '/'
        if not path.startswith("/"):
            return {
                "status": 400,
                "error": f"Bad Request: Invalid path '{path}'"
            }
        
        # 6. Valida la versión HTTP (solo soporta HTTP/1.1)
        if http_version != "HTTP/1.1":
            return {
                "status": 505,
                "error": f"HTTP Version Not Supported: {http_version}"
            }
        
        # --- Validación de headers ---
        headers = {}
        for line in lines[1:]:  # Itera desde la segunda línea
            # 7. Detecta fin de headers (línea vacía)
            if not line.strip():
                break
            
            # 8. Verifica formato de header (debe contener ": ")
            if ": " not in line:
                return {
                    "status": 400,
                    "error": f"Bad Request: Invalid header '{line}'"
                }
            
            # 9. Divide cada header en nombre y valor
            key, value = line.split(": ", 1)  # Split en el primer ": "
            headers[key.strip()] = value.strip()  # Guarda sin espacios
        
        # 10. Valida header Host obligatorio (requerido en HTTP/1.1)
        if "Host" not in headers:
            return {
                "status": 400,
                "error": "Bad Request: Missing 'Host' header"
            }
        
        # --- Validación del cuerpo (body) ---
        # 11. Encuentra el inicio del body (después de doble CRLF)
        body_index = lines.index("") + 1 if "" in lines else len(lines)
        body = "\r\n".join(lines[body_index:])  # Reconstruye el body
        
        # 12. Si existe Content-Length, verifica coincidencia con body real
        if "Content-Length" in headers:
            expected_length = int(headers["Content-Length"])
            if len(body) != expected_length:
                return {
                    "status": 400,
                    "error": "Bad Request: Incorrect body length"
                }
        
        # --- Si pasa todas las validaciones ---
        return {
            "status": 200,
            "error": None  # Indica que la solicitud es válida
        }

    except Exception as e:
        # Captura cualquier error inesperado durante la validación
        return {
            "status": 500,
            "error": f"Internal Server Error: {e}"
        }