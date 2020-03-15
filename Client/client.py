import socket
from tkinter import *
from tkinter import messagebox
from wikipedia import Wikipedia
import errno
import pandas as pd

#Network Configuration
HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 8000
username = "The Doctor"

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

def send_message(message):
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message.encode('utf-8'))

def recieve_message():
    try:
        while True:
            message_header = client_socket.recv(HEADER_LENGTH)

            if not len(message_header):
                return False
            
            message_length = int(message_header.decode('utf-8').strip())
            return {'header': message_header, 'data': client_socket.recv(message_length)}
    
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            messagebox.showerror("Reading Error", "Exiting")
            exit(-1)

#Second Frame button's functions
def send_person(code, query):
    message = f"{code}\n{query}"
    send_message(message)

def add_entry():
    wiki = Wikipedia(url_entry.get())
    name, birthday, deathday = wiki.scrap_person()
    query = name + "\n" + birthday + "\n" + deathday
    send_person("1", query)
    message = recieve_message()
    message = message['data'].decode('utf-8')
    if message == "OK":
        messagebox.showinfo("Operation Successful!", "Person was successfully added to the database")

    else:
        messagebox.showwarning("Operation Failed.", "Person exists on the database already.")

def delete_entry():
    send_person("2", name_entry.get())
    message = recieve_message()
    message = message['data'].decode('utf-8')
    if message == "OK":
        messagebox.showinfo("Operation Successful!", "Person was successfully deleted from the database")

    else:
        messagebox.showwarning("Operation Failed.", "Person doesn't exist on the database.")

#First frame button's functions
def get_people():
    send_message("3")
    people = recieve_message()
    if people is None:
        people = recieve_message()

    return people["data"].decode("utf-8")

people = []

def refresh():
    try:
        global people
        listbox.delete(0, END)
        people = get_people()
        for person in people.split("\n"):
            person = person.split(",")
            listbox.insert(END, person[1].replace("'", ""))

    except:
        pass

def extract():
    csv_file = csv.writer(open('data.csv', 'wb'), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_file.writerow(['NAME'] + ['SURNAME'] + ['AGE'])

    for person in people.split("\n"):
        person = person.split(' ')
        csv_file.writerow([person[0]] + person[1] + person[2])

def plot():
    pass

#Change frame function
def raise_frame(frame):
    frame.tkraise()

#GUI Configuration
top = Tk()
top.title("Wikipedia Data Mining")

#Main Frame configuration
frame1 = Frame(top)
list_frame = Frame(frame1)
button_frame1 = Frame(frame1)

listbox = Listbox(list_frame)
listbox.pack()
list_frame.pack()

save_button = Button(button_frame1, text="Extract", command=extract)
save_button.pack(side=LEFT)
plot_button = Button(button_frame1, text="Show Plot", command=plot)
plot_button.pack(side=LEFT)
refresh_button = Button(button_frame1, text="Refresh", command=refresh)
refresh_button.pack(side=LEFT)
conf_button = Button(button_frame1, text="Add/Delete User", command=lambda:raise_frame(frame2))
conf_button.pack(side=RIGHT)
button_frame1.pack()

#Secondary Frame configuration
frame2 = Frame(top)
url_frame = Frame(frame2)
name_frame = Frame(frame2)
button_frame2 = Frame(frame2)

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

add_button = Button(button_frame2, text="Add", command=add_entry)
add_button.pack(side=LEFT)
delete_button = Button(button_frame2, text="Delete", command=delete_entry)
delete_button.pack(side=LEFT)
return_button = Button(button_frame2, text="Back", command=lambda:raise_frame(frame1))
return_button.pack(side=RIGHT)
button_frame2.pack()

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="news")

try:
    get_people()

except:
    get_people()

raise_frame(frame1)
top.mainloop()
