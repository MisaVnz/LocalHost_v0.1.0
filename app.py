class MyWebApp:
    def handle_route(self, method, path, headers, body):
        """Método que maneja las rutas y devuelve contenido dinámico"""
        if path == "/":
            return (200, "<h1>Alfin se logro :)</h1><p>Denme ya mi titulo :(</p>", "text/html")
        elif path == "/about":
            return (200, "<h1>Acerca de</h1><p>Esta es una página de un estudiante que quiere graduarse</p>", "text/html")
        elif path == "/api/data":
            if method == "GET":
                return (200, '{"data": [1, 2, 3]}', "application/json")
            else:
                return (405, "Método no permitido", "text/plain")
        else:
            return (404, "Página no encontrada", "text/plain")