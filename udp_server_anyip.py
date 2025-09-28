import socket
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <IP_SERVIDOR> <PUERTO>")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"Servidor UDP escuchando en {HOST}:{PORT}")
        try:
            while True:
                data, client_address = server_socket.recvfrom(1024)
                message = data.decode()
                print(f"Mensaje recibido de {client_address}: {message}")
                response = f"Servidor recibió: {message}"
                server_socket.sendto(response.encode(), client_address)
        except KeyboardInterrupt:
            print("\nServidor UDP detenido.")
