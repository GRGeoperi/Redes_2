import socket

HOST = "localhost"  # El hostname o IP del servidor
PORT = 54321  # El puerto que usa el servidor
bufferSize = 1024
msgFromServer = "Archivo recibido correctamente (UDP)"
bytesToSend = str.encode(msgFromServer)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    print("Servidor UDP activo, esperando archivo...")
    with open("hamlet_recibido_udp.txt", "wb") as f:
        while True:
            data, address = UDPServerSocket.recvfrom(bufferSize)
            if data == b"__FIN_ARCHIVO__":
                print("Fin de archivo recibido.")
                # Enviar confirmación al cliente
                UDPServerSocket.sendto(bytesToSend, address)
                break
            f.write(data)
