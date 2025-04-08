from server import TCPServer
from app import MyWebApp

# Crear la aplicación web
app = MyWebApp()

# Crear y configurar el servidor
server = TCPServer(app)

if __name__ == "__main__":
    # Iniciar el servidor
    server.run()
