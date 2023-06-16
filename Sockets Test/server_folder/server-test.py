import requests

# Set the server address to the ngrok URL
SERVER_ADDRESS = 'https://47f7-121-200-4-145.ngrok-free.app'

# Add a new client to the server
response = requests.post(f'{SERVER_ADDRESS}/new_client', json={'ip': '127.420.69.1'})
print(response.status_code)
if response.status_code == 200:
    print('Client added to server')

# Send a message to the server
message = 'Hello, server!'
response = requests.post(f'{SERVER_ADDRESS}/send', json={'message': message})
print(response.status_code)
if response.status_code == 200:
    print(f'Message sent to server: {message}')

# Receive a message from the server
response = requests.post(f'{SERVER_ADDRESS}/receive')
print(response)
if response.status_code == 200:
    message = response.json()['message']
    print(f'Message received from server: {message}')