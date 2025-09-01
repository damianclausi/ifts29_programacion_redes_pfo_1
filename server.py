import socket
import sqlite3
import threading
import datetime
import sys

# Configuración del socket TCP/IP
def initialize_socket(host='localhost', port=5000):
    """Inicializa el socket del servidor y lo configura para escuchar conexiones."""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Servidor escuchando en {host}:{port}")
        return server_socket
    except socket.error as e:
        print(f"Error al inicializar el socket: {e}")
        sys.exit(1)

# Configuración de la base de datos SQLite
def initialize_database():
    """Crea o conecta a la base de datos SQLite y asegura que la tabla exista."""
    try:
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        sys.exit(1)

# Guardar mensaje en la base de datos
def save_message(conn, content, client_ip):
    """Guarda un mensaje en la base de datos con su timestamp y la IP del cliente."""
    try:
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().isoformat()
        cursor.execute('INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)',
                      (content, timestamp, client_ip))
        conn.commit()
        return timestamp
    except sqlite3.Error as e:
        print(f"Error al guardar el mensaje: {e}")
        return None

# Manejo de cada cliente en un hilo separado
def handle_client(client_socket, client_address):
    """Procesa los mensajes recibidos de un cliente y responde con confirmación."""
    print(f"Nueva conexión desde {client_address}")
    # Cada hilo crea su propia conexión a la base de datos
    conn = initialize_database()
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Mensaje recibido de {client_address}: {data}")
            # Guardar mensaje en la base de datos
            timestamp = save_message(conn, data, client_address[0])
            if timestamp:
                response = f"Mensaje recibido: {timestamp}"
                client_socket.send(response.encode('utf-8'))
            else:
                client_socket.send("Error al guardar el mensaje".encode('utf-8'))
        except socket.error as e:
            print(f"Error en la conexión con {client_address}: {e}")
            break
    conn.close()
    client_socket.close()
    print(f"Conexión cerrada con {client_address}")

# Aceptar conexiones de clientes
def accept_connections(server_socket, conn):
    """Acepta conexiones entrantes y delega su manejo a hilos separados."""
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except socket.error as e:
            print(f"Error al aceptar conexión: {e}")
            break

# Función principal del servidor
def main():
    """Configura el servidor y la base de datos, y comienza a escuchar conexiones."""
    server_socket = initialize_socket()
    conn = initialize_database()  # Solo para crear la tabla si no existe
    conn.close()
    try:
        accept_connections(server_socket, None)
    except KeyboardInterrupt:
        print("Cerrando servidor...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()