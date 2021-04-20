import socket, threading


# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

#create multithreaded function/class to address the bellow

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)
    
    print('server is up!!!!')

    #parse headers
    headers = request.split('/n')
    filename = headers[0].split()[1]
    
    #get content of the file
    if filename == '/':
        filename = 'ipsum.html'
    else:
        filename = filename[1:]
   
    try:
        file=open(filename)
        content = file.read()
        file.close()
        response = 'HTTP/1.0 200 OK\n\n'+content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found4'
    
    #response = 'HTTP/1.0 200 OK\n\n server is up'
    print('filename: '+ filename)


    
    
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()

