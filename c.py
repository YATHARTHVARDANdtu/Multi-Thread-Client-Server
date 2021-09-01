import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    msg = input("enter username :- ")
    client.send(msg.encode(FORMAT))
    connected = True
    while True:

        nmsg = client.recv(1024).decode(FORMAT)
        print(nmsg + "\n")
        nmsg = client.recv(1024).decode(FORMAT)
        print(nmsg + "\n")
       # nmsg = client.recv(1024).decode(FORMAT)
        #print(nmsg + "\n")

        msg = input(">")
        client.send(msg.encode(FORMAT))
        msg = input(">")
        client.send(msg.encode(FORMAT))



if __name__ == "__main__":
    main()