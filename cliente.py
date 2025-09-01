import socket
import sys

# Conexión al servidor
def connect_to_server(host='localhost', port=5000):
    """Inicializa el socket del cliente y se conecta al servidor."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Conectado a {host}:{port}")
        return client_socket
    except socket.error as e:
        print(f"Error al conectar con el servidor: {e}")
        sys.exit(1)

# Enviar mensajes al servidor
def send_messages(client_socket):
    """Permite al usuario enviar mensajes hasta que escriba 'éxito'."""
    while True:
        try:
            message = input("Escribe un mensaje (o 'éxito' para salir): ")
            if message.lower() == 'éxito':
                break
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Respuesta del servidor: {response}")
        except socket.error as e:
            print(f"Error al enviar/recibir mensaje: {e}")
            break
    client_socket.close()

# Función principal del cliente
def main():
    """Inicia el cliente y maneja la conexión."""
    client_socket = connect_to_server()
    send_messages(client_socket)

if __name__ == "__main__":
    main()