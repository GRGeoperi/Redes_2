import socket
import selectors
import time
import hashlib
import os

clients = {}  # Almacena info por cliente: archivo, bytes, tiempo, etc.

def accept(sock, mask):
    conn, addr = sock.accept()
    print('Conexión aceptada de', addr)
    conn.setblocking(False)
    # Nombre de archivo único por cliente
    filename = f"MobyDick_recibido_{addr[0].replace('.', '_')}_{addr[1]}.txt"
    f = open(filename, 'wb')
    clients[conn] = {
        'file': f,
        'addr': addr,
        'total_received': 0,
        'start_time': time.time(),
        'filename': filename
    }
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    BUFFER_SIZE = 1024
    data = conn.recv(BUFFER_SIZE)
    if data:
        clients[conn]['file'].write(data)
        clients[conn]['total_received'] += len(data)
    else:
        # Fin de transferencia
        clients[conn]['file'].close()
        end_time = time.time()
        addr = clients[conn]['addr']
        filename = clients[conn]['filename']
        print(f"\nCliente {addr} terminó la transferencia.")
        print(f"Archivo guardado como: {filename}")
        print(f"Total de bytes recibidos: {clients[conn]['total_received']}")
        print(f"Tiempo de transferencia: {end_time - clients[conn]['start_time']:.4f} segundos")
        # Calcular e imprimir checksum
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
            print("Checksums:")
            for alg in ["md5", "sha256"]:
                rec = calcular_checksum(filename, alg)
                print(f"{alg.upper()} recibido: {rec}")
        except Exception as e:
            print(f"No se pudo calcular el checksum: {e}")
        # Enviar confirmación
        try:
            conn.sendall(b"Archivo recibido correctamente")
        except Exception as e:
            print(f"No se pudo enviar confirmación: {e}")
        sel.unregister(conn)
        conn.close()
        del clients[conn]


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <IP_SERVIDOR> <PUERTO>")
        sys.exit(1)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    sel = selectors.DefaultSelector()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(100)
        sock.setblocking(False)
        sel.register(sock, selectors.EVENT_READ, accept)
        print(f"Servidor TCP escuchando en {HOST}:{PORT} (no bloqueante, múltiples clientes)")
        try:
            while True:
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        except KeyboardInterrupt:
            print("\nServidor TCP detenido.")
        finally:
            for c in clients.values():
                try:
                    c['file'].close()
                except Exception:
                    pass
