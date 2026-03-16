import socket
import os

HOST = "localhost"
PORT = 5000

input_folder = "../input"
output_folder = "../output"

os.makedirs(output_folder, exist_ok=True)

while True:

    files = os.listdir(input_folder)

    print("\nAvailable files:\n")

    for i, f in enumerate(files):
        print(i+1, ":", f)

    choice = int(input("\nSelect file number: ")) - 1

    filename = files[choice]

    path = os.path.join(input_folder, filename)

    ext = filename.split(".")[-1].lower()

    if ext == "png":
        conversion = "PNG2JPG"
        out_ext = "jpg"

    elif ext in ["jpg","jpeg"]:
        conversion = "JPG2PNG"
        out_ext = "png"

    elif ext == "webp":
        conversion = "WEBP2JPG"
        out_ext = "jpg"

    else:
        print("Unsupported file")
        continue

    print("Sending", filename)

    with open(path,"rb") as f:
        data = f.read()

    s = socket.socket()
    s.connect((HOST,PORT))

    s.sendall(conversion.ljust(10).encode())
    s.sendall(str(len(data)).ljust(16).encode())
    s.sendall(data)

    size = int(s.recv(16).decode().strip())

    result = b''

    while len(result) < size:
        result += s.recv(4096)

    output_file = os.path.join(output_folder, filename.split(".")[0]+"."+out_ext)

    with open(output_file,"wb") as f:
        f.write(result)

    print("Saved:",output_file)

    s.close()

    again = input("\nRun another conversion? (y/n): ")

    if again.lower() != "y":
        print("Exiting client...")
        break