import socket
from tkinter import *
from functools import partial
from threading import Thread

PORT = 14754
class RelaySwitch:
    def __init__(self, switch_id, button):
        self.switch_id = switch_id
        self.state = False
        self.button = button

def toggle_switch(switch, button):
    switch.state = not switch.state
    if switch.state:
        button.config(bg="green")
        message = "status_r10=r{}=1\r\n".format(switch.switch_id)
    else:
        button.config(bg="red")
        message = "status_r10=r{}=0\r\n".format(switch.switch_id)
    client_socket.send(message.encode())

def send_message():
    key = text_field1.get()
    value = text_field2.get()
    message = "{}={}".format(key, value)
    client_socket.send(message.encode())

def receive_message():
    while True:
        message = client_socket.recv(1024).decode()
        text_area.delete('1.0', END)
        text_area.insert(END, message + "\n")

        lines = message.split('\n')
        for line in lines:
            if line.startswith('r') and '=' in line:
                relay, state = line.split('=')
                relay_number = int(relay[1:]) - 1
                state = int(state)
                if int(state) == 1:
                    switches[relay_number].state = True
                    switches[relay_number].button.config(bg="green") 
                else:
                    switches[relay_number].state = False
                    switches[relay_number].button.config(bg="red")


root = Tk()
root.title("Ten-way Relay")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', PORT))

switches = []

for i in range(10):
    button_text = "Switch {}".format(i+1)
    switch_button = Button(root, text=button_text, bg="red")
    switch = RelaySwitch(i+1, switch_button)
    switch_button.config(command=partial(toggle_switch, switch, switch_button))
    if i < 5:
        switch_button.grid(row=i, column=0, padx=10, pady=10)
    else:
        switch_button.grid(row=i-5, column=2, padx=10, pady=10)
    switches.append(switch)

def send_status():
    message = "Status?"
    client_socket.send(message.encode())

key_label = Label(root, text="Key")
key_label.grid(row=5, column=0, padx=10, pady=10)

value_label = Label(root, text="Value")
value_label.grid(row=5, column=2, padx=10, pady=10)

text_field1 = Entry(root)
text_field1.grid(row=6, column=0, padx=10, pady=10)

text_field2 = Entry(root)
text_field2.grid(row=6, column=2, padx=10, pady=10)

send_button = Button(root, text="Send Message", command=send_message)
send_button.grid(row=7, column=1, padx=10, pady=10)

get_live_button = Button(root, text="Get Live", command=send_status)
get_live_button.grid(row=8, column=1, padx=10, pady=10)

text_area = Text(root)
text_area.grid(row=9, column=0, columnspan=3, padx=10, pady=10)

receive_thread = Thread(target=receive_message)
receive_thread.start()

root.mainloop()