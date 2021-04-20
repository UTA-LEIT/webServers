from io import SEEK_CUR
import socket, threading
import time


class serverthread(threading.Thread):
    def __init__(self,serverport):
        threading.Thread.__init__(self)
        self.serverport = serverport
        self.serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connectionThreads = []

    def run(self):
        self.serversocket.bind(('0.0.0.0', self.serverport))
        self.serversocket.listen(1)
        while True:
            #establish connection
            print('listening on... '+str(self.serverport))
            client_connection,client_address = self.serversocket.accept()
            request = client_connection.recv(1024).decode('utf-8')
            print('message received from: '+request)
            #print (request)
            self.connectionThreads.append(connectionThread(client_connection,request))
            self.connectionThreads[-1].daemon = 1
            self.connectionThreads[-1].start()

    def kill(self):
        for t in self.connectionThreads:
            try:
                t.connsocket.shutdown(socket.SHUT_RDWR)
                t.connsocket.close()
            except socket.error:
                pass
        t.connsocket.shutdown(socket.SHUT_RDWR)
        t.connsocket.close()

    
class connectionThread(threading.Thread):
    def __init__(self,connSocket,request):
        threading.Thread.__init__(self)
        self.connsocket = connSocket
        self.request = request

    def run(self):
        try:
            headers = self.request.split('/n')
            filename = headers[0].split()[1]
            
            if filename == '/':
                filename = 'ipsum.html'
            else:
                filename = filename[1:]

            file = open(filename)
            content = file.read()
            file.close()
            print('we are sleeping...')
            time.sleep(5)
            self.connsocket.send(b'HTTP/1.0 200 OK\n\n')
            for i in range(0,len(content)):
                codedcontent = content[i].encode()
                self.connsocket.send(codedcontent)
        except IOError:
            self.connsocket.send(b'HTTP/1.0 404 NOT FOUND\n')
        finally:
            self.connsocket.shutdown(socket.SHUT_RDWR)
            self.connsocket.close()



def main():
    server = serverthread(8080)
    server.daemon =1
    server.start()
    input('Press enter to exit...')
    server.close()
    print('Program complete')

if __name__ == '__main__':
    main()