import socket

#Network Configuration
HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 8000
message = "OK"

#Client Configuration
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(message_header + message.encode('utf-8'))
