
import socket
import time
import filecmp

HOST = "localhost"  # El hostname o IP del servidor
PORT = 54321  # El puerto que usa el servidor
bufferSize = 1024
msgFromServer = "Archivo recibido correctamente (UDP)"
bytesToSend = str.encode(msgFromServer)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    print("Servidor UDP activo, esperando archivo...")
    total_received = 0
    start_time = time.time()
    with open("hamlet_recibido_udp.txt", "wb") as f:
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
        iguales = filecmp.cmp("hamlet_recibido_udp.txt", "hamlet.txt", shallow=False)
        if iguales:
            print("El archivo recibido es idéntico al original (UDP, sin pérdidas detectadas).")
        else:
            print("El archivo recibido NO es idéntico al original (UDP, posibles pérdidas de datos).")
    except Exception as e:
        print(f"No se pudo comparar archivos: {e}")
