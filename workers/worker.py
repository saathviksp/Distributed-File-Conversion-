import socket
from PIL import Image
import io
import sys

WORKER_ID = sys.argv[1]
PORT = int(sys.argv[2])


def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", PORT))
server.listen()

print(f"[STARTED] Worker {WORKER_ID} on port {PORT}")

while True:

    try:

        conn, addr = server.accept()

        print(f"[{WORKER_ID}] Received job")

        conv_bytes = recv_exact(conn, 10)
        if not conv_bytes:
            conn.close()
            continue

        conv_type = conv_bytes.decode().strip()

        print(f"[{WORKER_ID}] Conversion requested: {conv_type}")

        size_bytes = recv_exact(conn, 16)
        if not size_bytes:
            conn.close()
            continue

        size = int(size_bytes.decode().strip())

        data = recv_exact(conn, size)

        print(f"[{WORKER_ID}] Processing file ({size} bytes)")

        img = Image.open(io.BytesIO(data))

        output = io.BytesIO()

        if conv_type == "PNG2JPG":
            img.convert("RGB").save(output, format="JPEG")

        elif conv_type == "JPG2PNG":
            img.save(output, format="PNG")

        elif conv_type == "PNG2WEBP":
            img.save(output, format="WEBP")

        elif conv_type == "WEBP2JPG":
            img.convert("RGB").save(output, format="JPEG")

        else:
            print(f"[{WORKER_ID}] Unsupported conversion")
            conn.close()
            continue

        result = output.getvalue()

        conn.sendall(str(len(result)).ljust(16).encode())
        conn.sendall(result)

        print(f"[{WORKER_ID}] Job finished")

        conn.close()

    except Exception as e:

        print(f"[{WORKER_ID}] ERROR:", e)