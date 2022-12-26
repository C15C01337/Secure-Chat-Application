import socket
import threading
from tkinter import *
import pickle
import rsa
import binascii


#defining the main window registration
rwindow = Tk()
rwindow.title("Registration Window | Created By Bishal Aryal")
rwindow.geometry('550x300')
rwindow['bg'] = '#00f7ff'

def printValue():
    global username
    username = player_name.get()
    Label(rwindow, text=f'{username}, Registered!', pady=20, bg='#00f7ff').pack()


player_name = Entry(rwindow)
player_name.pack(pady=30)

Button(
    rwindow,
    text="Register User", 
    padx=10, 
    pady=5,
    command=printValue
    ).pack()

#exit button
exit_button = Button(rwindow, text="Exit", command=rwindow.destroy)
exit_button.pack(pady=20)
rwindow.mainloop()
# end of registration window:

public, private = rsa.generate_keypair(1024)
msg=pickle.dumps(public)
print(public[0])

def ip_add():
    ip = change_ip.get()
    port = edit_text_port.get()
    # Define Client and connect to server:
    global client
    client = socket.socket()
    client.connect((ip, int(port)))
    # distryo input root
    root_window.destroy()
    # end of input root:
    root_window.quit()


def send():
    if str(edit_text.get()).strip() != "":
        message = str.encode(edit_text.get())
        hex_data   = binascii.hexlify(message)
        plain_text = int(hex_data, 16)
        ctt=rsa.encrypt(plain_text,pkey)
        client.send(str(ctt).encode())
        dmsg = edit_text.get()
        # print(dmsg)
        listbox.insert(END, username +" : "+ str(dmsg))
        edit_text.delete(0, END)

def recv():
    while True:
        response_message =int(client.recv(1024).decode())
        print(response_message)
        decrypted_msg = rsa.decrypt(response_message, private)
        # scrollbar:
        listbox.insert(END, name1 +" : "+ str(decrypted_msg))
        


# Client GUI
# Input Root_window GUI
root_window = Tk()
bgimage = PhotoImage(file ="imaged.png")

Label(root_window,image=bgimage).place(relwidth=1,relheight=1)
change_ip = Entry()
edit_text_port = Entry()
ip_label = Label(root_window, text="Enter Server IP")
port_label = Label(root_window, text="Enter Server Port")
connect_btn = Button(root_window, text="Connect To Server", command=ip_add, bg='#668cff', fg="white")

# show elements:
ip_label.pack(fill=X, side=TOP)
change_ip.pack(fill=X, side=TOP)
port_label.pack(fill=X, side=TOP)
edit_text_port.pack(fill=X, side=TOP)
connect_btn.pack(fill=X, side=BOTTOM)

root_window.title('Welcome'+' '+username +' | ' + 'Created By Bishal Aryal')
root_window.geometry("550x750")
root_window.resizable(width=False, height=False)

root_window.mainloop()

#sending details
name1=client.recv(1024).decode()
client.send(str.encode(username))
#receving details from server that is public key
rmsg=client.recv(1024)
pkey=pickle.loads(rmsg)

#client is a global variable to connect to server
client.send(msg)

# 2: Main Root GUI
root = Tk()
root.title("Created By: Bishal Aryal | Batch 30 Ethical")
bgimage2 = PhotoImage(file ="imaged.png")
Label(root,image=bgimage2).place(relwidth=1,relheight=1)
# Scrollbar:
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(root, yscrollcommand=scrollbar.set)
listbox.pack(fill=BOTH, side=TOP)
scrollbar.config(command=listbox.yview)

button = Button(root, text="Click to Send Message", command=send, bg='#4040bf', fg="white")

#exit button
exit_button = Button(root, text="Exit", command=root.destroy)
exit_button.pack(padx=10, pady=5, side=BOTTOM)

#here fill x mean filling all the x axis
button.pack(fill=X, side=BOTTOM)
edit_text = Entry(root)
edit_text.pack(fill=X, side=BOTTOM)

root.title('Welcome' +' '+ username +' | ' + 'Secure Chat Application')
root.geometry("700x750")
root.resizable(width=True, height=True)

threading.Thread(target=recv).start()

root.mainloop()