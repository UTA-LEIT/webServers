import socket

server = '0.0.0.0' #ip of the machine hosting the server
port =8080
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#AF_INET = socketFamily, SOCK_STREAM=socket kind
client.connect((server,port)) #connect defined client to <server> at <port>
client.sendall(bytes('this is from client','utf-8'))#send string as bytes coded by utf-8
while True:
    in_data = client.recv(1024)#Receive data up to 1024 bytes(coded by server)
    print('From Server: ',in_data.decode())# print in prompt From Server + data received and decode it
    out_data = input()#read data from input
    client.sendall(bytes(out_data,'utf-8'))#send everything from out_data coded by utf-8, to socket
    if out_data =='bye':#exit code
        break
client.close()#close socket after finish comunication