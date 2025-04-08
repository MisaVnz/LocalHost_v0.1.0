from server.config import Constants

class RequestHandler:
    def __init__(self, app=None):
        """Inicializa el manejador de peticiones HTTP"""
        # app: Aplicación externa que contendrá la lógica de negocio/ruteo
        self.app = app  # Puede ser None inicialmente
    
    def set_app(self, app):
        """Configura la aplicación externa que manejará el contenido"""
        self.app = app
    
    def handle_request(self, request):
        """
        Procesa una solicitud HTTP cruda y genera una respuesta HTTP.
        
        Parámetros:
            request (str): La solicitud HTTP completa como string
        
        Retorna:
            str: Respuesta HTTP formateada
        """
        try:
            # Divide el request por líneas (separadas por CRLF)
            lines = request.split("\r\n")
            
            # La primera línea es la línea de solicitud (ej: "GET / HTTP/1.1")
            request_line = lines[0]
            
            # Divide la línea de solicitud en sus componentes
            method, path, _ = request_line.split()  # _ ignora la versión HTTP
            
            # Extraer headers ---------------------------------------------------
            headers = {}
            for line in lines[1:]:  # Itera desde la segunda línea
                if not line.strip():  # Si encuentra línea vacía, fin de headers
                    break
                if ": " in line:  # Los headers válidos contienen ": "
                    key, value = line.split(": ", 1)  # Divide en el primer ": "
                    headers[key] = value  # Guarda el header en el diccionario
            
            # Extraer body -----------------------------------------------------
            body = ""
            if "\r\n\r\n" in request:  # El body está después de doble CRLF
                # Divide solo en la primera ocurrencia (por si el body contiene CRLF)
                _, body = request.split("\r\n\r\n", 1)
            
            # Delegar lógica a la aplicación externa ---------------------------
            if self.app:  # Si hay una aplicación configurada
                # La app debe implementar handle_route con esta interfaz:
                status, content, content_type = self.app.handle_route(
                    method=method,    # GET/POST/etc.
                    path=path,        # Ruta solicitada (/about, etc.)
                    headers=headers,  # Diccionario con headers
                    body=body         # Cuerpo del request (para POST/PUT)
                )
            else:  # Comportamiento por defecto si no hay app
                status, content, content_type = self._default_response(path)
            
            # Construir respuesta HTTP ------------------------------------------
            # Formato: "HTTP/1.1 {status}\r\nContent-Type: {type}\r\n\r\n{content}"
            return (
                f"HTTP/1.1 {status}\r\n"
                f"Content-Type: {content_type}"
                f"{Constants.END_HEADERS}"
                f"{content}"
            )
        
        except Exception as e:  # Captura cualquier error no previsto
            # Respuesta de error genérico (500 Internal Server Error)
            return (
                f"HTTP/1.1 500 Internal Server Error\r\n"
                f"Content-Type: text/plain"
                f"{Constants.END_HEADERS}"
                f"Server error: {str(e)}"
            )
    
    def _default_response(self, path):
        """
        Proporciona respuestas básicas cuando no hay aplicación configurada.
        
        Parámetros:
            path (str): Ruta solicitada
        
        Retorna:
            tuple: (status_code, content, content_type)
        """
        if path == "/":
            return (200, "Hola, esta es la página principal.", "text/plain")
        elif path == "/about":
            return (200, "Esta es la página 'Acerca de'.", "text/plain")
        else:
            return (404, "Página no encontrada.", "text/plain")
