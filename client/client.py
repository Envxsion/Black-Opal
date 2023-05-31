import socket

HOST = 'your_serveo_url'
PORT = 8000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            command = input('Enter command: ')
            s.sendall(command.encode())
            data = s.recv(1024)
            print(data.decode())

if __name__ == '__main__':
    main()