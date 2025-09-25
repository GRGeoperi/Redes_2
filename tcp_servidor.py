import hashlib
#!/usr/bin python3

import socket
import time
import filecmp

HOST = "10.100.84.82"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432 # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(5)
    print("El servidor TCP está disponible y en espera de solicitudes")

    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        print("Conectado a", Client_addr)
        total_received = 0
        start_time = time.time()
        with open("MobyDick_recibido_tcp.txt", "wb") as f:
            while True:
                data = Client_conn.recv(buffer_size)
                if not data:
                    print("No se recibieron más datos. Fin de la transferencia.")
                    break
                f.write(data)
                total_received += len(data)
        end_time = time.time()
        print(f"Total de bytes recibidos: {total_received}")
        print(f"Tiempo de transferencia: {end_time - start_time:.4f} segundos")
        # Comprobar si el archivo recibido es igual al original
        try:
            iguales = filecmp.cmp("MobyDick_recibido_tcp.txt", "MobyDick.txt", shallow=False)
            if iguales:
                print("El archivo recibido es idéntico al original.")
            else:
                print("El archivo recibido NO es idéntico al original.")
        except Exception as e:
            print(f"No se pudo comparar archivos: {e}")
        # Calcular e imprimir checksum MD5 y SHA256 de ambos archivos
        def calcular_checksum(path, algoritmo):
            h = hashlib.new(algoritmo)
            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    h.update(chunk)
            return h.hexdigest()

        try:
            print("\nChecksums:")
            for alg in ["md5", "sha256"]:
                orig = calcular_checksum("MobyDick.txt", alg)
                rec = calcular_checksum("MobyDick_recibido_tcp.txt", alg)
                print(f"{alg.upper()} original:  {orig}")
                print(f"{alg.upper()} recibido: {rec}")
                if orig == rec:
                    print(f"Los archivos son idénticos según {alg.upper()}\n")
                else:
                    print(f"Los archivos son diferentes según {alg.upper()}\n")
        except Exception as e:
            print(f"No se pudo calcular el checksum: {e}")
        # Enviar confirmación después de recibir todo el archivo
        mensaje_confirmacion = "Archivo recibido correctamente".encode()
        Client_conn.sendall(mensaje_confirmacion)
