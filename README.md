# IFTS 29 - Tecnicatura en Desarrollo de Software  
## Programación sobre redes - 3° D

### Práctica Formativa Obligatoria 1

**Alumno:** Damián Andrés Clausi  
**Profesor:** Germán Ríos  


# Chat Básico Cliente-Servidor con Sockets y Base de Datos

## Descripción
Este proyecto implementa un sistema de chat básico en Python utilizando sockets TCP/IP y una base de datos SQLite. Permite que múltiples clientes se conecten a un servidor, envíen mensajes y que estos mensajes se almacenen en una base de datos junto con la fecha y la IP del cliente.

## Estructura del Proyecto
- `server.py`: Código del servidor. Escucha conexiones, recibe mensajes y los guarda en la base de datos.
- `cliente.py`: Código del cliente. Permite enviar mensajes al servidor y muestra la respuesta.
- `chat.db`: Base de datos SQLite donde se almacenan los mensajes.

## Requisitos
- Python 3.x
- Módulo estándar `sqlite3` (incluido en Python)

## Ejecución
### 1. Iniciar el Servidor
Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python3 server.py
```

El servidor escuchará en `localhost:5000` y creará la base de datos `chat.db` si no existe.

### 2. Iniciar el Cliente
En otra terminal, en la misma carpeta, ejecuta:

```bash
python3 cliente.py
```

El cliente se conectará al servidor y podrás enviar mensajes. Escribe `éxito` para finalizar la sesión.

### 3. Consultar los Mensajes Guardados
Para ver los mensajes almacenados en la base de datos, ejecuta:

```bash
sqlite3 chat.db "SELECT * FROM mensajes;"
```

## Notas
- El servidor maneja múltiples clientes usando hilos.
- Cada mensaje se almacena con su contenido, fecha de envío e IP del cliente.
- El código está modularizado y documentado para facilitar su comprensión.
