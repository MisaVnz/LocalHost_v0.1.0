import signal
import socket
from server.config import Config
from server.router import RequestHandler
from server.validate_request import validate_request

running = True

class TCPServer:
    def __init__(self, app=None):
        """Inicializa el servidor TCP con una aplicación opcional"""
        # Crea un manejador de peticiones y le pasa la aplicación
        self.handler = RequestHandler(app)
    
    def set_app(self, app):
        """Permite cambiar/setear la aplicación externa en tiempo de ejecución"""
        self.handler.set_app(app)
    
    def run(self):
        """Método principal que inicia y ejecuta el servidor"""
        global running  # Hace referencia a la variable global
        
        # Configura el manejador para la señal SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, self._handle_sigint)

        # Crea el socket del servidor:
        # - socket.create_server es un helper para crear sockets TCP
        # - (Config.HOST, Config.PORT) define la dirección y puerto
        # - reuse_port=False evita reusar el puerto inmediatamente tras cerrar
        server_socket = socket.create_server((Config.HOST, Config.PORT), reuse_port=False)
        print(f"Server escuchando en {Config.PORT}...")

        # Bucle principal del servidor - se ejecuta mientras running == True
        while running:
            try:
                # Acepta una nueva conexión:
                # - accept() bloquea hasta que llega una conexión
                # - client_socket: nuevo socket para comunicarse con este cliente
                # - client_address: tupla (IP, puerto) del cliente
                client_socket, client_address = server_socket.accept()
                print(f"Conexión desde {client_address}")

                # Usa 'with' para asegurar que el socket se cierre correctamente
                with client_socket:
                    # Recibe datos del cliente:
                    # - recv() lee hasta BUFFER_SIZE bytes
                    # - decode() convierte de bytes a string
                    data = client_socket.recv(Config.BUFFER_SIZE).decode()
                    
                    # Valida la solicitud HTTP:
                    # - validate_request devuelve un dict con status/error
                    validation_result = validate_request(data)
                    
                    # Si la validación falla (status != 200)
                    if validation_result["status"] != 200:
                        # Construye una respuesta de error HTTP
                        response = f"HTTP/1.1 {validation_result['status']} {validation_result['error']}\r\nContent-Type: text/plain\r\n\r\n"
                        # Envía la respuesta codificada a bytes
                        client_socket.send(response.encode())
                        print(f"Estado de conexion: {validation_result['status']}")
                        continue  # Vuelve al inicio del bucle

                    # Si la validación es exitosa, maneja la petición:
                    # - handler.process_request genera la respuesta HTTP
                    response = self.handler.handle_request(data)
                    
                    # Envía la respuesta al cliente
                    client_socket.send(response.encode())
                    print(f"Estado de conexion: 200")

            # Captura Ctrl+C directamente (como respaldo del manejador de señales)
            except KeyboardInterrupt:
                print("\nServidor interrumpido por el usuario. Apagándose...")
                break  # Sale del bucle principal
            
            # Captura cualquier otro error inesperado
            except Exception as e:
                print(f"Error: {e}")
                break  # Sale del bucle principal

        # Limpieza final:
        print("Cerrando el socket del servidor...")
        server_socket.close()  # Cierra el socket del servidor
    
    def _handle_sigint(self, signum, frame):
        """Manejador de señal para Ctrl+C (SIGINT)"""
        global running
        print("\nReceived SIGINT. Apagando el servidor...")
        running = False  # Cambia la condición del bucle principal