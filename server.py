from tkinter import *
import rsa
import pickle
import socket
import binascii
import threading

#defining the main window registration
rwindow = Tk()
rwindow.title("Registration Window | Created By Bishal Aryal")
rwindow.geometry('550x300')
rwindow['bg'] = '#ffbf00'

def printValue():
    global username
    username = player_name.get()
    Label(rwindow, text=f'{username}, Registered!', pady=20, bg='#ffbf00').pack()


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

public, private = rsa.generate_keypair(1024)
#creating a serialized message in the form of byte array of the public key to transfer it to the client
msg=pickle.dumps(public)
print(public[0])

def ip_add():
    ip = change_ip.get()
    port = edit_text_port.get()
    
    # Define Server:
    server = socket.socket()
    server.bind((ip, int(port)))
    server.listen()

    global conn
    conn, addr = server.accept()

    # distroying the main root window
    root_window.destroy()
    # quiting the main root window
    root_window.quit()

def send():
    if str(edit_text.get()).strip() != "":
        message = str.encode(edit_text.get())
        #converting it into number to understand clearly
        hex_data   = binascii.hexlify(message)
        # print(hex_data)

        plain_text = int(hex_data, 16)
        # print(plain_text)

        #encrypting the message using the public key of server
        ciphertext=rsa.encrypt(plain_text,pkey)
        conn.send(str(ciphertext).encode())

        # scrollbar feature:
        #listbox to insert the chat data
        dmsg = edit_text.get()
        # print(dmsg)
        listbox.insert(END, username +" : "+ str(dmsg))
        edit_text.delete(0, END)

    # after sending the message
    edit_text.delete(0, END)

def recv():
    while True:
        response_message =int(conn.recv(1024).decode())
        print(response_message)
        decrypted_msg = rsa.decrypt(response_message, private)
        #scrollbar feature :
        listbox.insert(END, name1 +" : "+ str(decrypted_msg))
        edit_text.delete(0, END)


# Server GUI:

# 1: Input Root GUI
root_window = Tk()
bgimage = PhotoImage(file ="imaged.png")
# bgimage = PhotoImage(file ="frontlogo.png")
Label(root_window,image=bgimage).place(relwidth=1,relheight=1)
change_ip = Entry()
edit_text_port = Entry()
ip_label = Label(root_window, text="Please enter the Enter IP address:")
port_label = Label(root_window, text="Port to listen connection:")
connect_btn = Button(root_window, text="Start a Server", command=ip_add, bg='#668cff', fg="white")

# show elements:
ip_label.pack(fill=X, side=TOP)
change_ip.pack(fill=X, side=TOP)
port_label.pack(fill=X, side=TOP)
edit_text_port.pack(fill=X, side=TOP)
connect_btn.pack(fill=X, side=BOTTOM)

root_window.title('Welcome'+' '+username +' | '+ 'Created By Bishal Aryal')
root_window.geometry("550x750")
root_window.resizable(width=False, height=False)

root_window.mainloop()

#sending details-----------
conn.send(str.encode(username))
name1=conn.recv(1024).decode()

#sending public key to client
conn.send(msg)
#receiving pub key from client
rmsg=conn.recv(1024)
#deserialize the byte array of pub key from client to orginal object using loads()
pkey=pickle.loads(rmsg)

#conn is a global variable to connect to client


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

button = Button(root, text="Click to Send Message", command=send, bg='#29a329', fg="white")

#exit button
exit_button = Button(root, text="Exit", command=root.destroy)
exit_button.pack(padx=10, pady=5, side=BOTTOM)

edit_text = Entry(root)
button.pack(fill=X, side=BOTTOM)
edit_text.pack(fill=X, side=BOTTOM)

root.title('Welcome' +' '+ username +' | ' + 'Secure Chat Application')
root.geometry("700x750")
root.resizable(width=True, height=True)

threading.Thread(target=recv).start()
root.mainloop()