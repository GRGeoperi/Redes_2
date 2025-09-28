import threading
import sys
import time
import socket

def udp_client(client_id, server_host, server_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            msg = f"Hola desde UDP cliente {client_id}".encode()
            sock.sendto(msg, (server_host, server_port))
            data, _ = sock.recvfrom(1024)
            print(f"UDP Cliente {client_id} recibió: {data.decode()}")
            time.sleep(1)
    except Exception as e:
        print(f"UDP Cliente {client_id} error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <IP_SERVIDOR> <PUERTO>")
        sys.exit(1)
    SERVER_HOST = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
    NUM_CLIENTS = 3
    threads = []
    for i in range(NUM_CLIENTS):
        t = threading.Thread(target=udp_client, args=(i, SERVER_HOST, SERVER_PORT))
        t.start()
        threads.append(t)
        time.sleep(0.5)  # Pequeño retardo para simular concurrencia
    for t in threads:
        t.join()
