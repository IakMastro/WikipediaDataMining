import socket
from tkinter import *
from tkinter import messagebox
from wikipedia import Wikipedia

#Network Configuration
HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 8000
username = "The Doctor"

def send_message(code, query):
    message = f"{code}\n{query}"
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message.encode('utf-8'))

def recieve_message():
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    
    except:
        return False

#Adding and deleting functions, accessed by the buttons
def add_entry():
    wiki = Wikipedia(url_entry.get())
    name, birthday, deathday = wiki.scrap_person()
    query = name + "\n" + birthday + "\n" + deathday
    send_message(1, query)
    message = recieve_message()
    message = message['data'].decode('utf-8')
    if message == "OK":
        messagebox.showinfo("Operation Successful!", "Person was successfully added to the database")

    else:
        messagebox.showwarning("Operation Failed.", "Person exists on the database already.")

def delete_entry():
    send_message(2, name_entry.get())
    message = recieve_message()
    message = message['data'].decode('utf-8')
    if message == "OK":
        messagebox.showinfo("Operation Successful!", "Person was successfully deleted from the database")

    else:
        messagebox.showwarning("Operation Failed.", "Person doesn't exist on the database.")

#GUI Configuration
top = Tk()
top.title("Wikipedia Data Mining")
url_frame = Frame(top)
name_frame = Frame(top)
button_frame = Frame(top)

url_label = Label(url_frame, text="URL")
url_label.pack(side=LEFT)
url_entry = Entry(url_frame, bd=5)
url_entry.pack(side=RIGHT)
url_frame.pack()

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
    message_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + username.encode('utf-8'))

except:
    messagebox.showerror("No Connection to Server", "ERROR 404: Couldn't connect to the server. Press OK to exit.")
    exit(-1)

top.mainloop()
