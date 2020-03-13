import socket
from tkinter import *
from tkinter import messagebox

#Network Configuration
HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 8000
message = "OK"

def add_entry():
    pass

def delete_entry():
    pass

top = Tk()
top.title("Wikipedia Data Mining")
name_frame = Frame(top)
button_frame = Frame(top)

name_label = Label(name_frame, text="Name")
name_label.pack(side=LEFT)
name_entry = Entry(name_frame, bd=5)
name_entry.pack(side=RIGHT)
name_frame.pack()

add_button = Button(button_frame, text="Add", command=add_entry)
add_button.pack(side=LEFT)
delete_button = Button(button_frame, text="Delete", command=delete_entry)
delete_button.pack(side=RIGHT)
button_frame.pack()

try:
    #Client Configuration
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message.encode('utf-8'))

except:
    messagebox.showerror("No Connection to Server", "ERROR 404: Couldn't connect to the server. Press OK to exit.")
    exit(-1)

top.mainloop()
