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
    seventh curl -v --data "12345" -H "Content-Type: application/octet-stream" http://localhost:4221/files/file_123 creates a directory and file if doesnt exist 
    eighth  curl -v -H "Accept-Encoding: gzip" http://localhost:4221/echo/abc response should include content encoding type and body is omitted
            curl -v -H "Accept-Encoding: invalid-encoding" http://localhost:4221/echo/abc if content encode type is not supported dont return type
    nineth  curl -v -H "Accept-Encoding: invalid-encoding-1, gzip, invalid-encoding-2" http://localhost:4221/echo/abc  
            curl -v -H "Accept-Encoding: invalid-encoding-1, invalid-encoding-2" http://localhost:4221/echo/abc multiple values if gzip is the content encoding return content encoding type
    tenth
    """
    
    print("Logs from your program will appear here!")

    """create a TCP/IP
       create_server(
        Tuple("ip of this device where the server is created", exposed port),   
        resuse_port=Bolean (*depends on OS you use reuse_port or not) allows multiple applications  to listen on the same port
        )"""
    server_socket = socket.create_server(("localhost", 4221)) 

    def list_to_dictionary(mylist):
        headers = {}
        for item in mylist:
            if ":" in item:
                key, value = item.split(": ", 1)  # Split only once to keep the entire header value together
                if "," in value:  # Check if the value contains a comma
                    # Split the value by comma to handle multiple values
                    values_list = value.split(", ")
                    headers[key] = values_list
                else:
                    headers[key] = value.strip()  # Remove leading/trailing whitespace
                    
        accept_encoding = headers.get('Accept-Encoding', [])
        if 'gzip' in accept_encoding:
            accept_encoding_value = 'gzip'
        elif accept_encoding == []:
            accept_encoding_value = 'empty'
        else:
            accept_encoding_value = 'unsupported'
        return accept_encoding_value

    def handle_req(client, addr):
        data = client.recv(1024).decode()
        req = data.split("\r\n")
        path = req[0].split(" ")[1]
        method = req[0].split(" ")[0]

        if path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif path.startswith("/echo"):
            if list_to_dictionary(req) == 'gzip':
               response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: {list_to_dictionary(req)}\r\n\r\n".encode()
            elif list_to_dictionary(req) == 'empty':
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}".encode()
            else:
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n".encode()
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
