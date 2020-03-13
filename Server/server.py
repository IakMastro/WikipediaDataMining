import socket
import select
from database import Database

#Coloured messages
BLUE = '\033[1;34m'
RED = '\033[0;31m'
GREEN = '\033[1;32m'
DEFAULT = '\033[0m'

#Network Configuration
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 8000

try:
    db = Database()

except:
    print(RED + f"Couldn't connect to the database. Exiting..." + DEFAULT)
    exit(-1)

#Server Configuration
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
socket_list = [server_socket]
clients = {}
print(BLUE + f"Listening for connections on " + GREEN + f"{IP}:{PORT}" + DEFAULT)

#Functions for recieving and sending messages
def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    
    except:
        return False

def send_message(client_socket, message):
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message.encode('utf-8'))

#Function adding and deleting persons from the database
def add_person(client_socket, name, birthday, deathday):
    if db.insert(name, birthday, deathday):
        send_message(client_socket, "OK")        

    else:
        send_message(client_socket, "ERROR: 402")

def delete_person(client_address, name):
    if db.delete(name):
        send_message(client_socket, "OK")
    
    else:
        send_message(client_socket, "ERROR: 402")

#Server Configuration
while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = recieve_message(client_socket)
            
            if user is False:
                continue

            socket_list.append(client_socket)
            clients[client_socket] = user
            print(BLUE + "Accepted new connection from " + GREEN +
             "{}:{}, message: {}".format(*client_address, user['data'].decode('utf-8')) + DEFAULT)

        else:
            message = recieve_message(notified_socket)

            if message is False:
                print(BLUE + f"Closed connection from: {clients[notified_socket]['data'].decode('utf-8')}" + DEFAULT)
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            message = message["data"].decode("utf-8")
            message = message.split('\n')

            if message[0] is "1":
                add_person(client_socket, message[1], message[2], message[3])

            elif message[0] is "2":
                delete_person(client_socket, message[1])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]
