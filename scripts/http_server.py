import socket

class SimpleHTTPServer:
    def __init__(self, host="0.0.0.0", port=8080):
        self.host = host
        self.port = port
        self.username = "user"
        self.password = "password123"
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server started at http://{self.host}:{self.port}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            request = client_socket.recv(1024).decode()
            if "POST /login" in request:
                self.handle_login(client_socket, request)
            else:
                self.send_response(client_socket, "HTTP/1.1 200 OK", "Welcome to the simple HTTP server!")

            client_socket.close()

    def handle_login(self, client_socket, request):
        lines = request.split("\r\n")
        for line in lines:
            if line.startswith("Content-Length:"):
                content_length = int(line.split(":")[1].strip())
        
        body = request[-content_length:]
        params = body.split("&")
        username = params[0].split("=")[1]
        password = params[1].split("=")[1]
        
        if username == self.username and password == self.password:
            self.send_response(client_socket, "HTTP/1.1 200 OK", "Login successful!")
        else:
            self.send_response(client_socket, "HTTP/1.1 401 Unauthorized", "Invalid credentials!")

    def send_response(self, client_socket, status_code, body):
        response = f"{status_code}\r\nContent-Type: text/html\r\n\r\n{body}"
        client_socket.sendall(response.encode())

if __name__ == "__main__":
    server = SimpleHTTPServer()
    server.start()