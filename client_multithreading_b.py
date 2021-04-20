import socket

server = '' #ip of the machine hosting the server
port =8080
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((server,port))
client.sendall(bytes('this is from client','utf-8'))
while True:
    in_data = client.recv(1024)
    print('From Server: ',in_data.decode())
    out_data = input()
    client.sendall(bytes(out_data,'utf-8'))
    if out_data =='bye':
        break
client.close()