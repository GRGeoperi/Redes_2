import selectors
import socket

sel = selectors.DefaultSelector()

# Creamos un socket UDP (no orientado a conexión)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", 12345))  # servidor escuchando en puerto 9999
sock.setblocking(False)


# Función que maneja eventos de lectura y escritura
def eventos(sock, mask):
    if mask & selectors.EVENT_READ:
        data, addr = sock.recvfrom(1024)  # recibe datos UDP
        print("Recibido:", data.decode(), "de", addr)
        # responder
        sock.sendto(b"ACK: " + data, addr)
    if mask & selectors.EVENT_WRITE:
        print("El socket está listo para escribir.")

# Registramos el socket para eventos de lectura y escritura con la misma función
sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, eventos)

print("Servidor UDP escuchando ")
try:
    while True:
        events = sel.select(timeout=None)  # espera eventos
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
except KeyboardInterrupt:
    print("Servidor detenido")
finally:
    sel.close()
    sock.close()