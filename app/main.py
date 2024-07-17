import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # first curl -v http://localhost:4221 to test the server if returns 200 ok message
    # second curl -v http://localhost:4221/abcdefg
    print("Logs from your program will appear here!")

    """create a TCP/IP
       create_server(
        Tuple("ip of this device where the server is created", exposed port),   
        resuse_port=Bolean (*depends on OS you use reuse_port or not) allows multiple applications  to listen on the same port
        )"""
    server_socket = socket.create_server(("localhost", 4221)) 
    """accept() accepts all ping from client device
        [0] is the tuple is returns the Tuple containing ip and port
        sendall() is sending response to devices whoever pings the server with the message inside of it 
        "b" the message response is sent as a byte string 
        \ r \ n \ r \ n  is needed to end the header and to indicate a transition to the body of the message """
    server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    
    

if __name__ == "__main__":
    main()
