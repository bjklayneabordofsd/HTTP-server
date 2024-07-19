import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # first curl -v http://localhost:4221 to test the server if returns 200 ok message
    # second curl -v http://localhost:4221/abcdefg return error if path is not found
    # third curl -v http://localhost:4221/echo/abc return body "abc" when using echo
    print("Logs from your program will appear here!")

    """create a TCP/IP
       create_server(
        Tuple("ip of this device where the server is created", exposed port),   
        resuse_port=Bolean (*depends on OS you use reuse_port or not) allows multiple applications  to listen on the same port
        )"""
    server_socket = socket.create_server(("localhost", 4221)) 

    while True:
        client_socket, addr = server_socket.accept()
        
        # Receive the entire request
        request = client_socket.recv(1024).decode('utf-8')
        print(request)
        
        # Simple path extraction (this is very basic and might not work for all cases)
        path = request.split(' ')[1]

        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith('/echo/'):
                endpoint_string = path[len("/echo/"):]
                content_length = len(endpoint_string)
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{endpoint_string}".encode('utf-8')
            
        
        client_socket.sendall(response)
        client_socket.close()
    
    

if __name__ == "__main__":
    main()
