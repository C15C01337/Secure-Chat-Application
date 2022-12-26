# Secure Chat Application
The purpose of this project is to design a chat application, also known as a secure chat application. The main purpose of the software is to provide users with an instant messaging tool that has the RSA key encryption in which user's private chat will be encrypted with the public key and secured while sending message, and can be decrypted with the user's private key.
The best encrypted messaging apps can help protect our privacy. This make it difficult for hackers to eavesdrop on our private chats because they can't crack the message only using the public key and encrypted message.

# RSA algorithm :
RSA is  asymmetric cryptography algorithm. Asymmetric actually means that it works on two different keys i.e. Public Key and Private Key. As the name describes that the Public Key is given to everyone and Private key is kept private.

An example of asymmetric cryptography :

A client (for example browser) sends its public key to the server and requests for some data.
The server encrypts the data using client’s public key and sends the encrypted data.
Client receives this data and decrypts it using it's private key
When client message to server it encrypt with server's public key and where server encrypt decrypt with it's private key.

Client recieve the public key of server and Server receives the public key of client during the inital connection.
### To Run The porgram First Run The server and open a port for connection

``` 
python ./server.py
```
 ### Now Run The client Script and connect to the host server
``` 
python ./client.py
```
# YouTube Video Link
[YouTube Video](https://youtu.be/O1EOcG3VZxM)