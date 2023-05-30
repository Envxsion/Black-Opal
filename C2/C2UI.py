import csv
import customtkinter as ctk
from PIL import Image, ImageTk, ImageChops
from CTkMessagebox import CTkMessagebox

app = ctk.CTk()
app.title("Black Opal Log In")
app.geometry("1264x800")
ctk.deactivate_automatic_dpi_awareness()



def c2_tab_generate():
    # Create C2 tab
    c2_tab = tabview.add("C2")
    # Switch to C2 tab
    tabview.set("C2")
def show_pass():
    if keyent.cget('show') == '*':
        keyent.configure(show='')
        showpas.configure(image=open_eye)
    else:
        keyent.configure(show='*')
        showpas.configure(image=closed_eye)

def show_man_page():
    tabview.set("Man Page")


def binary_search(arr, x):
    # Returns index of x in arr if present, else -1
    l = 0
    r = len(arr) - 1
    while l <= r:
        mid = l + (r - l) // 2
        if arr[mid][0] == x:
            return mid
        elif arr[mid][0] < x:
            l = mid + 1
        else:
            r = mid - 1
    return -1

def login():
    usr = userent.get()
    key = keyent.get()

    # Check if username and password are in datastore.csv using binary search
    with open('datastore.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = sorted(list(reader), key=lambda x: x[0])
        index = binary_search(rows, usr)
        if index != -1:
            if rows[index][1] == key:
                CTkMessagebox(title='Log in successful', message= f'Hello {usr}')
                c2_tab_generate()
                return
            else:
                CTkMessagebox(title="ERROR",message="Key is incorrect!", icon="cancel")
        else:
            # If username and password are not found in datastore.csv
            CTkMessagebox(title="ERROR",message="You are not authorised to log in!", icon="cancel")
def themed():
    if themeswitch.get() == 0:
        ctk.set_appearance_mode("Dark")
        themeswitch.configure(text="🌙")
    if themeswitch.get() == 1:
        ctk.set_appearance_mode("Light")
        themeswitch.configure(text="☀️")


# Create tab view
tabview = ctk.CTkTabview(app)
tabview.pack(padx=0, pady=0,expand=1, fill="both")

# Create Login tab
login_tab = tabview.add("Login")


banner = ctk.CTkCanvas(login_tab, width=750, height=350)
banner.place(x=250, y=-4)
banneri = Image.open("Resources/Banner.png")
bannerimg = ImageChops.offset(banneri, -80, 0)
bannerimg = ImageTk.PhotoImage(bannerimg)
banner.create_image(490, 150, image=bannerimg)

userlbl = ctk.CTkLabel(login_tab, text="USR:",font=("Arial",20,"bold"))
userlbl.place(x=500,y=400)

userent = ctk.CTkEntry(login_tab, placeholder_text="AAA0001",font=("Arial",20,"bold"))
userent.place(x=580,y=400)
keylbl = ctk.CTkLabel(login_tab, text="KEY:",font=("Arial",20,"bold"))
keylbl.place(x=500,y=450)

keyent = ctk.CTkEntry(login_tab, show="*", placeholder_text="********",font=("Arial",20,"bold"))
keyent.place(x=580,y=450)
keyent.bind("<Return>", lambda e: login())

loginbtn = ctk.CTkButton(login_tab, text="Login",font=("Arial",20,"bold"),command=login)
loginbtn.place(x=550,y=530)

open_eye = ctk.CTkImage(Image.open("Resources/eye_open.png"))
closed_eye = ctk.CTkImage(Image.open("Resources/eye_closed.png"))
showpas = ctk.CTkButton(master=login_tab,text="",width=1,image=closed_eye, command=show_pass)
showpas.place(x=730,y=452)

# Create Man Page tab
man_page_tab = tabview.add("Man Page")

# Help Icon
info = ctk.CTkImage(Image.open("Resources/info_help_icon.png"))
helpbtn = ctk.CTkButton(master=login_tab,text="",width=20,image=info, command=show_man_page, compound="top", fg_color="#18445a",bg_color="#18445a")
helpbtn.place(x=banner.winfo_x() + banner.winfo_width() - helpbtn.winfo_width(), y=10)

# Create C2 tab
#c2_tab = tabview.add("C2")


# Check if user is logged in
# Doesnt work, tabs don't have states (normal and disabled)
#if tabview.get() == "C2" and userent.get() != "KEK0001":
#    print(tabview.get())
#    print(userent.get())
#    print("test")
#    CTkMessagebox(title="ERROR", message="Please log in first", icon="cancel")
#    tabview.set("Login")
#else:
#    print(tabview.get())
#    print(userent.get())

themeswitch = ctk.CTkSwitch(app,text="🌙",command=themed)
themeswitch.place(x=10,y=770)

app.mainloop()         
 
    



