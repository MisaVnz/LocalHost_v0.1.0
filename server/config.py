
class Constants:
    CRLF = "\r\n"
    END_HEADERS = CRLF + CRLF
    CONTENT_TYPE = "Content-Type: HTML"
    RESPONSE_200 = "HTTP/1.1 200 OK" + CRLF + CONTENT_TYPE + END_HEADERS + "<h1>QUE BUENO, ESTA FUNCIONANDO :)</h1>"

class Config:
    # Variables de configuracion del server
    HOST = "localhost"
    PORT = 7725
    BUFFER_SIZE = 1024

class Security:
    MAX_HEADERS_SIZE = 8192  
    MAX_BODY_SIZE = 1024 * 1024 * 10  
    ALLOWED_METHODS = {"GET", "POST"}
    BANNED_PATHS = {"/.env", "/.git"} # Prevenir acceso a archivos sensibles