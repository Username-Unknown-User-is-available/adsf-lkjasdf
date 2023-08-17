import socket
from threading import Thread

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipaddress="127.0.0.1"
port=8000

server.bind((ipaddress, port))
server.listen()
listofclients=[]

print("Server is Running. :)")

def clientThread(connection, adress):
    connection.send("Wellcome to this chatroom.".encode("utf-8"))
    while True:
        try:
            message=connection.recv(2048).decode("utf-8")
            if message:
                print("<"+adress[0]+">"+message)
                messagetosend="<"+adress[0]+">"+message
                broadcast(messagetosend, connection)
            else:
                remove(connection)
        except:
            continue
def broadcast(message, connection):
    for client in listofclients:
        if client!=connection:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove(client)

def remove(connection):
    if connection in listofclients:
        listofclients.remove(connection)

while True:
    connection,adress=server.accept()
    listofclients.append(connection)
    print(adress[0]+ " Connected")

    newthread=Thread(target=clientThread, args=(connection, adress))
    newthread.start()