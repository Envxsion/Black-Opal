import paramiko

# Set up SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to remote machine using ngrok tunnel
ngrok_url = "https://7d3c-103-205-229-1.au.ngrok.io"
ssh.connect(ngrok_url, port=22, username="your-username-here", password="your-password-here")

# Run commands on the remote machine
stdin, stdout, stderr = ssh.exec_command("your-command-here")
print(stdout.read())
