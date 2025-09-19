import socket

HOST = "localhost"  # El hostname o IP del servidor
PORT = 54321  # El puerto usado por el servidor
serverAddressPort = (HOST, PORT)
bufferSize = 1024
file_path = "hamlet.txt"

# Crea un socket UDP del lado del cliente
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPClientSocket:
    # Enviar el archivo en fragmentos
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(bufferSize)
            if not chunk:
                break
            UDPClientSocket.sendto(chunk, serverAddressPort)
    # Enviar mensaje especial para indicar fin de archivo
    UDPClientSocket.sendto(b"__FIN_ARCHIVO__", serverAddressPort)
    # Esperar confirmación del servidor
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    print("Mensaje del servidor {}".format(msgFromServer[0]))




    