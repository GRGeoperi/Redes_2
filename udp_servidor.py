import hashlib

import socket
import os
import time
import filecmp

HOST = "10.100.84.82"  # El hostname o IP del servidor
PORT = 54321  # El puerto que usa el servidor
bufferSize = 1024
msgFromServer = "Archivo recibido correctamente (UDP)"
bytesToSend = str.encode(msgFromServer)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    print("Servidor UDP activo, esperando archivo...")
    total_received = 0
    start_time = time.time()
    with open("MobyDick_recibido_udp.txt", "wb") as f:
        while True:
            data, address = UDPServerSocket.recvfrom(bufferSize)
            if data == b"__FIN_ARCHIVO__":
                print("Fin de archivo recibido.")
                end_time = time.time()
                # Enviar confirmación al cliente
                UDPServerSocket.sendto(bytesToSend, address)
                break
            f.write(data)
            total_received += len(data)
    print(f"Total de bytes recibidos: {total_received}")
    print(f"Tiempo de transferencia: {end_time - start_time:.4f} segundos")
    # Comprobar si el archivo recibido es igual al original
    try:
        iguales = filecmp.cmp("MobyDick_recibido_udp.txt", "MobyDick.txt", shallow=False)
        if iguales:
            print("El archivo recibido es idéntico al original (UDP, sin pérdidas detectadas).")
        else:
            print("\033[91mADVERTENCIA: El archivo recibido NO es idéntico al original (UDP, posibles pérdidas de datos).\033[0m")
            # Mostrar diferencia de bytes
            try:
                original_size = os.path.getsize("MobyDick.txt")
                recibido_size = os.path.getsize("MobyDick_recibido_udp.txt")
                diff = original_size - recibido_size
                if diff > 0:
                    print(f"Faltan {diff} bytes en el archivo recibido.")
                elif diff < 0:
                    print(f"El archivo recibido tiene {abs(diff)} bytes extra.")
                else:
                    print("Los archivos tienen el mismo tamaño pero diferente contenido.")
            except Exception as e:
                print(f"No se pudo calcular la diferencia de tamaño: {e}")
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
        rec = calcular_checksum("MobyDick_recibido_udp.txt", alg)
        print(f"{alg.upper()} original:  {orig}")
        print(f"{alg.upper()} recibido: {rec}")
        if orig == rec:
            print(f"Los archivos son idénticos según {alg.upper()}\n")
        else:
            print(f"Los archivos son diferentes según {alg.upper()}\n")
except Exception as e:
    print(f"No se pudo calcular el checksum: {e}")
