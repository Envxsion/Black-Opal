#python c:\Users\cyn0v\Documents\GitHub\Black-Opal\Tron\Tron.py --tunnel serveo --subdomain envxsion2048 -p 80



import requests

# Replace the URL with the public URL of your Tron.py server
url = "https://cbe2-121-200-4-145.ngrok-free.app"

def download_file(url,file_path):
    # Download the file from the server
    url = f"{url}/{file_path}"
    response = requests.get(url)

    # Save the file to disk
    with open(file_path, "wb") as f:
        f.write(response.content)

def upload_file(url, file_path):
    # Upload the file to the server
    url = url + "/upload/" + file_path
    with open(file_path, "rb") as f:
        response = requests.put(url, data=f.read())

def make_file(file_path):
    # Create a new file on the server
    url = url + "make " + file_path
    response = requests.put(url)

def delete_file(file_path):
    # Delete a file on the server
    url = url + "delete " + file_path
    response = requests.delete(url)

while True:
    # Get user input
    command = input("Enter command: ")

    # Check if the command is a download request
    if command.startswith("download "):
        # Extract the file path from the command
        file_path = command.split(" ")[1]

        # Download the file from the server
        download_file(url,file_path)

    # Check if the command is an upload request
    elif command.startswith("upload "):
        # Extract the file path from the command
        file_path = command.split(" ")[1]

        # Upload the file to the server
        upload_file(url,file_path)

    # Check if the command is a make file request
    elif command.startswith("make "):
        # Extract the file path from the command
        file_path = command.split(" ")[1]

        # Create a new file on the server
        make_file(url,file_path)

    # Check if the command is a delete file request
    elif command.startswith("delete "):
        # Extract the file path from the command
        file_path = command.split(" ")[1]

        # Delete a file on the server
        delete_file(url,file_path)

    else:
        # Send the command to Tron.py
        response = requests.post(url, data=command)

        # Print Tron.py's output
        print(response.text)