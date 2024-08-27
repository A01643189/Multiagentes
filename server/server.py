import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
from agent import test  # Assuming agent.py is in the same directory as server.py

class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        response_data = get_response()
        self._set_response()
        self.wfile.write(str(response_data).encode('utf-8'))


    def post_response(data):
    # Process the data as needed
        response_data = {
            "status": "success",
            "message": "Data received and processed",
            "received_data": data
        }
        return json.dumps(response_data)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                    str(self.path), str(self.headers), json.dumps(post_data))
    
        # Process the POST data
        response_data = post_response(post_data)
        
        self._set_response()
        self.wfile.write(response_data.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")
    try:
        httpd.serve_forever()  # This should keep the server running indefinitely
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

# Adjust this to make sure the server keeps running
if __name__ == '__main__':
    from sys import argv
    
    # Iniciar hilo del servidor    
    server_thread = threading.Thread(target=run, args=tuple(), daemon=True)
    server_thread.start()
    
    # Optionally run the test or simulation
    # If test() is necessary, ensure it doesn't stop the server
    # test()
    
    # Keep the main thread running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("Server stopped by user.")
