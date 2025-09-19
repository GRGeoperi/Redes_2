#!/usr/bin python3
import socket

HOST = "localhost"  # Hostname o dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024
file_path = "hamlet.txt"  # Ruta absoluta al archivo

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando archivo hamlet.txt...")
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(buffer_size)
            if not chunk:
                break
            TCPClientSocket.sendall(chunk)
    TCPClientSocket.shutdown(socket.SHUT_WR)
    print("Esperando una respuesta...")
    try:
        data = TCPClientSocket.recv(buffer_size)
        if data:
            print("Recibido:", repr(data))
        else:
            print("No se recibió respuesta del servidor.")
    except OSError as e:
        print(f"Error al recibir datos: {e}")
