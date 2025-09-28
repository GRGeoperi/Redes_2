import socket
import selectors

def accept(sock, mask):
    conn, addr = sock.accept()
    print('Conexión aceptada de', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print('Recibido:', data.decode(), 'de', conn.getpeername())
        conn.sendall(data)
    else:
        print('Cerrando conexión con', conn.getpeername())
        sel.unregister(conn)
        conn.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <IP_SERVIDOR> <PUERTO>")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    sel = selectors.DefaultSelector()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(100)
        sock.setblocking(False)
        sel.register(sock, selectors.EVENT_READ, accept)
        print(f"Servidor TCP escuchando en {HOST}:{PORT}")
        try:
            while True:
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        except KeyboardInterrupt:
            print("\nServidor TCP detenido.")
