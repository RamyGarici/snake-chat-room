import socket
import threading


HOST = '127.0.0.1'
PORT = 4444

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        client_socket.sendall(data)




def start_server():
    s = socket.socket()
    s.bind((HOST,PORT))
    s.listen()
    while True:

        client_socket,addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
    