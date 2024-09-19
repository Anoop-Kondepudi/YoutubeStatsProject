import http.server
import socketserver
import webbrowser
import threading

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

# Function to start the server
def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Open the website in the default web browser
webbrowser.open(f"http://localhost:{PORT}/index.html")

# Keep the script running until the server is stopped manually
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nServer stopped.")