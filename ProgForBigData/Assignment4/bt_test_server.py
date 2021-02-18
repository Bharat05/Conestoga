""" Server for multithreated (asynchronous chat) application 
Adapted from https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170"""

import socket
# from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address} has connected.")
        client.send(
            bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = f"Welcome {name}! If you ever want to quit, type 'quit' to exit."
    client.send(bytes(welcome, "utf8"))
    clients[client] = name
    client_count = len(clients)
    msg = f"{name} has just been connected. Total connections is {client_count}."
    broadcast(bytes(msg, "utf8"))

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("quit", "utf8"):

            broadcast(msg, time.ctime() + ' ' + name + ": ")
        else:
            client.send(bytes("quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} has left the chat.", "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


# Defining constants
clients = {}
addresses = {}

HOST = socket.gethostbyname(socket.gethostname())
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
