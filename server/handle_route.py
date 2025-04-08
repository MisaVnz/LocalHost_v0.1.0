def handle_route(self, method, path, headers, body):
    # method: "GET", "POST", etc.
    # path: "/about", "/users", etc.
    # headers: Diccionario con los headers HTTP
    # body: String con el cuerpo del request (para POST/PUT)
    status_code = "" # int
    content = "" # str
    content_type = "" # str
    return (status_code, content, content_type)