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
        while True:
            print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size)
            print ("Recibido,", data,"   de ")
            if not data:
                break
            print("Enviando respuesta a", Client_addr)
            # Enviar solo una confirmación al finalizar la recepción
            break
        # Enviar confirmación después de recibir todo el archivo
        mensaje_confirmacion = "Archivo recibido correctamente".encode()
        Client_conn.sendall(mensaje_confirmacion)
