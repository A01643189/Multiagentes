# TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
# Python server to interact with Unity via POST
# Sergio Ruiz-Loza, Ph.D. March 2021
# Actualizado por Axel Dounce, PhD

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import threading
from server.agent import test

class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        response_data = get_response()
        self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        self.wfile.write(str(response_data).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        #post_data = self.rfile.read(content_length)
        post_data = json.loads(self.rfile.read(content_length))
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     #str(self.path), str(self.headers), post_data.decode('utf-8'))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), json.dumps(post_data))
      
      
        # Aquí se procesa lo el cliente ha enviado, y se construye una respuesta.
        response_data = post_response(post_data)
        
        
        self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self.wfile.write(str(response_data).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")
    
    #======================Procesamiento de datos de cliente=========================
    
def post_response(data):
    """
    Función para procesar los datos que vienen del cliente (mediante POST) en forma de JSON.
    Se construye un JSON para la respuesta al cliente.
    Se retorna la respuesta.
    
    Ejemplo:
    
        x = data['x'] * 2
        y = data['y'] * 2
        z = data['z'] * 2
        
        new_position = {
            "x" : x+1,
            "y" : y-1,
            "z" : z
        }
        
        return new_position
    """
    
    return None

def get_response(data):
    """
    Función construir un JSON para la respuesta al cliente (GET).
    Se retorna la respuesta.
    
    Ejemplo:
    
        act = wealth_transfer
        
        
        return act
    """
    
    return None
    
    
#===================Definición de Agentes y simulación (Model)=================
#
#


    
#
#
# 



#==================================Main===========================

if __name__ == '__main__':
    from sys import argv
    
    #Iniciar hilo del servidor    
    p = threading.Thread(target=run, args = tuple(),daemon=True)
    p.start()
    test()
    #Correr simulación (de preferencia no especifiquen los steps)
    



