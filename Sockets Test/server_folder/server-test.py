import requests

# Set the server address to the ngrok URL
SERVER_ADDRESS = 'https://f8d6-121-200-4-145.ngrok-free.app'

# Add a new client to the server
requests.post(f'{SERVER_ADDRESS}/new_client', json={'ip': '127.0.0.1'})

# Send a message to the client
message = 'Hello, client!'
response = requests.post(f'{SERVER_ADDRESS}/send', json={'message': message})
if response.status_code == 200:
    print(f'Message sent to client: {message}')

# Receive a message from the client
response = requests.post(f'{SERVER_ADDRESS}/receive')
if response.status_code == 200:
    message = response.json()['message']
    print(f'Message received from client: {message}')