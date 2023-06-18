from datetime import datetime
import requests
from os import makedirs, path

# Consts
BUFFER_SIZE = 1024
POWER_MODULE_COOLDOWN = 5  # Minutes
SCREENSHOT_COOLDOWN = 0.5  # Minutes
UPDATE_TABLE_COOLDOWN = 3000  # Milliseconds
SERVER = 'http://localhost:8000'  # Change the server address to match your server's address
WIN = None

# Server Variables
client_list = []
targets = []


def send_to_client(target, message, response=True, as_bytes=False):
    """
    Sends a message to a client
    :param target: Number of client
    :param message: Message
    :param response: Whether or not the function will wait for a response from the client
    :param as_bytes: Whether or not the return would come in a decoded str form, or a byte form
    :return: response from the client or None of client lost connection to the server (If receive is enabled)
    """
    try:
        conn = client_list[target]['data']['socket']
        response = requests.post(SERVER, data=message)
        if response.status_code == 200:
            server_response = response.content
            if server_response is None:
                delete_client(target)
                return ''
            return server_response
    except requests.exceptions.RequestException as e:
        print('Error: ' + str(e))
        delete_client(target)
        if response is True:
            return ''


def delete_client(target):
    """
    Deletes a target from the client list. Should be used when a client is dead.
    :param target: Number of client
    """
    print('Connection to client #{} was lost... Removing client...'.format(target + 1))
    client_list[target]['data']['socket'].close()
    client_list.pop(target)  # Delete dead client from the list

    # Fix targets list to match new client list.
    for i in range(len(targets)):
        if targets[i] > target:
            targets[i] = targets[i] - 1
        elif targets[i] == target:
            targets.pop(i)  # Delete dead client from targets list



