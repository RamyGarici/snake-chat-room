import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 4444

rooms = {}


def broadcast(room_name, message, sender_socket=None):
    data = json.dumps({"text":message}).encode('utf-8')
    for client in rooms[room_name]:
        if client!= sender_socket:
            client.send(data)
        


def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        message = json.loads(data)
        action = message.get("action")
        if action == "join":
            username = message.get("username")
            current_room = message.get("room")
            if current_room not in rooms:
                rooms[current_room]={}
            rooms[current_room][client_socket]= username
            broadcast(current_room,message,client_socket)
        elif action == "message":
            message_text = message.get("text")
            broadcast(current_room,f"{username}: {message_text}",client_socket)








def start_server():
    s = socket.socket()
    s.bind((HOST,PORT))
    s.listen()
    while True:

        client_socket,addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
    