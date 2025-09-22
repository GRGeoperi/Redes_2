import socket
import time

HOST = "localhost"  # El hostname o IP del servidor
PORT = 54321  # El puerto usado por el servidor
serverAddressPort = (HOST, PORT)
bufferSize = 1024
file_path = "hamlet.txt"

# Crea un socket UDP del lado del cliente
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPClientSocket:
    total_sent = 0
    start_time = time.time()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(bufferSize)
            if not chunk:
                break
            UDPClientSocket.sendto(chunk, serverAddressPort)
            total_sent += len(chunk)
            print(f"Enviado: {total_sent} bytes", end='\r')
            time.sleep(0.001)  # Pequeño retardo para evitar saturar el buffer
    end_time = time.time()
    print(f"\nArchivo '{file_path}' enviado completamente.")
    print(f"Total de bytes enviados: {total_sent}")
    print(f"Tiempo de transferencia: {end_time - start_time:.4f} segundos")
    # Enviar mensaje especial para indicar fin de archivo
    UDPClientSocket.sendto(b"__FIN_ARCHIVO__", serverAddressPort)
    # Esperar confirmación del servidor
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    print("Mensaje del servidor {}".format(msgFromServer[0]))
