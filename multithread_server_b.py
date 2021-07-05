import socket
from _thread import *
import threading
import time
import random

class ClientThread(threading.Thread):#Class that will listen to client connections
    def __init__(self,clientAdress,clientSocket):#init of class
        threading.Thread.__init__(self) #init of a thread
        self.csocket = clientSocket #store a possible client socket connection into a variable
        print ('New Connection added: ', clientAddress)
    def run(self):#method that represents thread activity. Overloaded
        print('connection from: ',clientAddress)
        self.csocket.send(bytes("hi this is from server..",'utf-8')) # send bytes to client socket as bytes coded by utf-8
        msg='' #variable messa empty
        while True:#keep alive forever
            data = self.csocket.recv(2048)#receive data at maximum size 2048
            msg=data.decode()#decode message because client will send it coded
            if msg=='bye':#exit message
                break
            #x= random.randint(1,10)#sleep for testing purposes
            x =2
            time.sleep(x)#sleep for testing purposes
            print('from client',msg)
            print('sleep time = '+str(x))
            self.csocket.send(bytes(msg,'utf-8'))#send msg bytecoded by'utf-8'
        print('client at ',clientAddress,' diconnected...')


localhost = '0.0.0.0'#host of server
port =8080 #port serving
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#initialize server socket(server family,socket kind)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#Socket behavior control. On some systems, sendmsg() and recvmsg() can be used to pass file descriptors between processes over an AF_UNIX socket. When this facility is used (it is often restricted to SOCK_STREAM sockets), recvmsg() will return, in its ancillary data, items of the form (socket.SOL_SOCKET, socket.SCM_RIGHTS, fds), where fds is a bytes object representing the new file descriptors as a binary array of the native C int type.
server.bind((localhost,port))#bind localhost to port
print('server started')
print('wait for client request..')

while True:#keep alive
    server.listen(1)# number of unaccepted connections that the system will allow before refusing new connections.
    clientsock,clientAddress = server.accept()# server accept clientsock at client address
    newthread = ClientThread(clientAddress,clientsock) #Define new thread for each connectioin
    newthread.start()#start the thread


