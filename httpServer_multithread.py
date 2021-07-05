from io import SEEK_CUR
import socket, threading
import time
import random


class serverthread(threading.Thread):
    """class that the server

    Args:
        threading ([Thread]): Thread descriptor
    """
    def __init__(self,serverport):
        """class init method
    Args:
        serverport ([string]): port of the socket
    """
        threading.Thread.__init__(self)
        self.serverport = serverport
        self.serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#initialize server socket(server family,socket kind)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#Socket behavior control. On some systems, sendmsg() and recvmsg() can be used to pass file descriptors between processes over an AF_UNIX socket. When this facility is used (it is often restricted to SOCK_STREAM sockets), recvmsg() will return, in its ancillary data, items of the form (socket.SOL_SOCKET, socket.SCM_RIGHTS, fds), where fds is a bytes object representing the new file descriptors as a binary array of the native C int type.
        self.connectionThreads = [] #save a list of connection threads

    def run(self):
        """Run method of class(overided)
        """
        self.serversocket.bind(('0.0.0.0', self.serverport)) #bind server address to port
        self.serversocket.listen(1)# number of unaccepted connections that the system will allow before refusing new connections.
        while True:
            #establish connection
            print('listening on... '+str(self.serverport))
            client_connection,client_address = self.serversocket.accept() #accept
            request = client_connection.recv(1024).decode('utf-8')#revceive at maxsize of 1024.decoded cause client will send coded content
            print('message received from: '+request)
            #print (request)
            self.connectionThreads.append(connectionThread(client_connection,request))#save in list 
            self.connectionThreads[-1].daemon = 1 # The significance of this flag is that the entire Python program exits when only daemon threads are left.
            self.connectionThreads[-1].start() #start thread even if no connections are added. (thread over thread)

    def kill(self):
        """Kill threads
        """
        for t in self.connectionThreads:
            try:
                t.connsocket.shutdown(socket.SHUT_RDWR)
                t.connsocket.close()
            except socket.error:
                pass
        t.connsocket.shutdown(socket.SHUT_RDWR)
        t.connsocket.close()

    
class connectionThread(threading.Thread):
    """Class that handles the thread connections

    Args:
        threading (thread): Thread
    """
    def __init__(self,connSocket,request):
        """init socket

        Args:
            connSocket (String): socket to be served
            request (request): request
        """
        threading.Thread.__init__(self)
        self.connsocket = connSocket
        self.request = request

    def run(self):
        try:
            headers = self.request.split('/n')#separate the requests by newline
            filename = headers[0].split()[1]#get 1st element
            
            if filename == '/': #configure root
                filename = 'ipsum.html'
            else:
                filename = filename[1:] #ads whatever we put into the filename

            file = open(filename) #open file
            content = file.read()#readfile
            x= random.randrange(1,10) #sleep for testing purposes
            print(threading.get_ident())#thread identification
            print('sleeping: '+str(x))#sleep for testing purposes
            time.sleep(x)#sleep for testing purposes
            file.close()
            self.connsocket.send(b'HTTP/1.0 200 OK\n\n') #send ok flag(200)
            for i in range(0,len(content)): #readfile char by char
                codedcontent = content[i].encode() #encode content
                self.connsocket.sendall(codedcontent)#send all once
        except IOError:#in case of input error
            self.connsocket.send(b'HTTP/1.0 404 NOT FOUND\n')
        finally:
            self.connsocket.shutdown(socket.SHUT_RDWR)#shutdown of the socket
            self.connsocket.close()



def main():
    server = serverthread(8020) #porta a servir pelo servidor
    server.daemon = 1 #background
    server.start()#start server
    input('Press enter to exit...')
    server.close()
    print('Program complete')

if __name__ == '__main__':
    main()