import socket
from _thread import *
import threading
import time

class ClientThread(threading.Thread):
    def __init__(self,clientAdress,clientSocket):
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        print ('New Connection added: ', clientAddress)
    def run(self):
        print('connection from: ',clientAddress)
        self.csocket.send(bytes("hi this is from server..",'utf-8'))
        msg=''
        while True:
            data = self.csocket.recv(2048)
            msg=data.decode()
            if msg=='bye':
                break
            time.sleep(2)
            print('from client',msg)
            #self.csocket.send(bytes(msg,'utf-8'))
        print('client at ',clientAddress,' diconnected...')


localhost = '0.0.0.0'
port =8080
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind((localhost,port))
print('server started')
print('wait for client request..')

while True:
    server.listen(1)
    clientsock,clientAddress = server.accept()
    newthread = ClientThread(clientAddress,clientsock)
    newthread.start()


