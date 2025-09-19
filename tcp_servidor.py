#!/usr/bin python3
import socket

HOST = "localhost"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432 # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(5)
    print("El servidor TCP está disponible y en espera de solicitudes")

    Client_conn, Client_addr = TCPServerSocket.accept()
    #Crear objeto thread (client_conn)
    with Client_conn:
        print("Conectado a", Client_addr)
        with open("hamlet_recibido_tcp.txt", "wb") as f:
            while True:
                print("Esperando a recibir datos... ")
                data = Client_conn.recv(buffer_size)
                if not data:
                    print("No se recibieron más datos. Fin de la transferencia.")
                    break
                print ("Recibido,", len(data), "bytes de", Client_addr)
                f.write(data)
        # Enviar confirmación después de recibir todo el archivo
        mensaje_confirmacion = "Archivo recibido correctamente".encode()
        Client_conn.sendall(mensaje_confirmacion)
