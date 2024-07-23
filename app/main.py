import socket
import threading
import sys
import os
def main():
    """
    You can use print statements as follows for debugging, they'll be visible when running tests.
    first curl -v http://localhost:4221 to test the server if returns 200 ok message
    second curl -v http://localhost:4221/abcdefg return error if path is not found
    third curl -v http://localhost:4221/echo/abc return body "abc" when using echo
    fourth curl -v --header "User-Agent: foobar/1.2.3" http://localhost:4221/user-agent return value header in response
    fifth   (sleep 3 && printf "GET / HTTP/1.1\ r\ n\ r\ n") | nc localhost 4221 &
            (sleep 3 && printf "GET / HTTP/1.1\ r\ n\ r\ n") | nc localhost 4221 &
            (sleep 3 && printf "GET / HTTP/1.1\ r\ n\ r\ n") | nc localhost 4221 &
            test multiple concurrent request 
    sixth echo -n 'Hello, World!' > /tmp/foo
          curl -i http://localhost:4221/files/foo response body should return file contents if file doesnt exist return 404
    """
    
    print("Logs from your program will appear here!")

    """create a TCP/IP
       create_server(
        Tuple("ip of this device where the server is created", exposed port),   
        resuse_port=Bolean (*depends on OS you use reuse_port or not) allows multiple applications  to listen on the same port
        )"""
    server_socket = socket.create_server(("localhost", 4221)) 

    def handle_req(client, addr):
        data = client.recv(1024).decode()
        req = data.split("\r\n")
        path = req[0].split(" ")[1]
        method = req[0].split(" ")[0]

        if path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif path.startswith("/echo"):
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}".encode()
        elif path.startswith("/user-agent"):
            user_agent = req[2].split(": ")[1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
        elif path.startswith("/files"):
            if method == "POST":
                body_start_index = data.find("\r\n\r\n") + 4
                body = data[body_start_index:].strip()
    
                # Extract the filename from the path, including the directory part
                filename = path[len("/files/"):]
    
                # Define the base directory where files will be stored
                base_directory = sys.argv[2]
    
                # Construct the full path where the file should be saved
                # This includes creating the directory if it doesn't exist
                filepath = os.path.join(base_directory, filename)
    
                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
                # Write the body to a file
                try:
                    with open(filepath, "w") as f:
                        f.write(body)
                    response = f"HTTP/1.1 201 Created\r\n\r\n".encode()
                except Exception as e:
                    response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: {len(str(e))}\r\n\r\nError creating file: {str(e)}".encode()
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        client.send(response)

    try:
        while True:
            client_socket, addr = server_socket.accept()

            # Start a new thread to handle the client connection
            thread = threading.Thread(target=handle_req, args=(client_socket, addr)).start()

    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_socket.close()
    

if __name__ == "__main__":
    main()
