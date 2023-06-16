from gui import start as start_gui
from threading import Thread
import requests
import sys
from pyngrok import ngrok
import subprocess
import requests
import os
import time
from pyuac import main_requires_admin
from flask import Flask, request, jsonify
from datetime import datetime
from os import makedirs, path

app = Flask(__name__)

SERVER_ADDRESS = None  # Define SERVER_ADDRESS as a global variable

class Server:
    client_connections = []

    def accept_connections(self):
        """
        Accepts new client connections and adds them to the client list
        """
        while True:
            client, address = self.server_socket.accept()
            log(f"Accepted a connection from {address[0]}:{address[1]}")
            self.client_connections.append(client)


    import datetime

    @app.route('/new_client', methods=['POST'])
    def new_client():
        """
        Adds a new client to the client list
        """
        client_data = request.json
        exist = False
        for client in Server.client_connections:
            if client.getpeername()[0] == client_data['ip']:
                exist = True
                break
        if not exist:
            log(f"New client connected: {client_data['ip']}. Request content: {request.get_data()}")
            Server.client_connections.append(requests)
            with open('client_data.txt', 'a') as f:
                f.write(f"{datetime.datetime.now()}: {client_data}\n")
        return jsonify({'status': 'success'})


    @app.route('/send', methods=['POST'])
    def send_message():
        """
        Sends a message to the client
        :param message: Message to send to the client (str)
        """
        message = request.json['message']
        compressed_message = message.encode()
        try:
            response = requests.post(f"{SERVER_ADDRESS}/receive", json={'message': compressed_message.decode()})
            if response.status_code != 200:
                print(f"Failed to send message: {response.text}")
            else:
                log(f"Sent message: {message}")
        except requests.exceptions.RequestException as e:   
            print(f"Failed to send message: {e}")
        return jsonify({'status': 'success'})


    @app.route('/receive', methods=['POST'])
    def receive_message():
        if request.method == 'POST':
            message = request.data.decode()
            log(f"Received message: {message}")
            # Process the message here
            return jsonify({'message': 'Message received: ' + str(message)})
        else:
            return jsonify({'error': 'Method not allowed'}), 405
    
    @app.route('/', methods=['GET','POST'])
    def index():
        if request.method == 'POST':
            message = request.data.decode()
            log(f"Received message: {message}")
            # Process the message here
            return jsonify({'message': 'Message received'} + str(message))
        else:
            return jsonify({'error': 'Method not allowed'}), 405

def log(message):
    """
    Logs a message to a log file in ./server_folder/logs
    :param message: Message to log
    """
    file_path = 'logs/BlackOpal-{}.log'.format(datetime.now().strftime('%d.%m.%Y'))
    makedirs(path.dirname(file_path), exist_ok=True)
    with open(file_path, 'a+') as f:
        f.write(datetime.now().strftime('[%d/%m/%Y %H:%M:%S]: ') + message + '\n')
        print('--------------------\n', message)

@app.before_request
def log_request_info():
    """
    Logs the request information
    """
    log(f"Request URL: {request.url}")
    log(f"Request method: {request.method}")
    log(f"Request headers: {request.headers}")
    log(f"Request data: {request.get_data()}")

@app.after_request
def log_response_info(response):
    """
    Logs the response information
    """
    log(f"Response status: {response.status}")
    log(f"Response headers: {response.headers}")
    log(f"Response data: {response.get_data()}")
    return response

@main_requires_admin
def main():
    global SERVER_ADDRESS  # Access the global variable
    # Default Server Parameters
    ip = 'localhost'
    port = 8000

    # Change IP and Port according to the startup args
    for arg in sys.argv[1:]:
        if arg.startswith('--ip=') or arg.startswith('-i='):
            ip_arg = arg.split('=', maxsplit=1)[1]
            print(ip_arg)
            if ip_arg != '':
                ip = ip_arg
            else:
                log('Invalid ip address was inputted.')
        elif arg.startswith('--port=') or arg.startswith('-p='):
            try:
                port = int(arg.split('=', maxsplit=1)[1])
            except ValueError as e:
                log(str(e))
                log('Inputted port number is invalid. Starting on default port')

    # Start the GUI in a separate thread
    gui_thread = Thread(target=start_gui, daemon=True)
    gui_thread.start()

    # Start the server
    try:
        # Step 0: Save the default path
        default_path = os.getcwd()
        print(default_path)
        # Step 1: cd into user's folder in Windows
        os.chdir(os.path.expanduser("~"))
        print("CD'd into user's folder in Windows")

        # Step 2: Start ngrok to expose the server to the internet
        ngrok_process = subprocess.Popen(["C:/Users/cyn0v/Documents/GitHub/Black-Opal/Resources/ngrok.exe", "http", "--host-header=rewrite", "8000"])
        print("Started ngrok to expose the server to the internet")
        time.sleep(2) # Give ngrok time to start up
        # Get the public URL from ngrok output
        public_url = requests.get("http://localhost:4040/api/tunnels").json()["tunnels"][0]["public_url"]
        log(f'Server is now publicly accessible at {public_url}')
        SERVER_ADDRESS = public_url  # Set the server address to the ngrok URL
        server = Server()
        server.server_socket = app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
        Thread(target=server.accept_connections, daemon=True).start()  # Thread to accept new connections
    except requests.exceptions.RequestException as e:
        log(str(e))
        log('Invalid IP address to host server on.')
    except OverflowError as e:
        log(str(e))
        log('Invalid Port number to host server on.')

if __name__ == "__main__":
    main()
