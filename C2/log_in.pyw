import customtkinter as ctk
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox


app = ctk.CTk()
app.title("Black Opal Log In")
app.geometry("1264x800")

banner = ctk.CTkCanvas(app, width=1582, height=260)
banner.place(x=-2, y=-4)
banneri = Image.open("Banner.png")
bannerimg = ImageTk.PhotoImage(banneri.resize((1582, 400)))
banner.create_image(792, 130, image=bannerimg)


def show_pass():
        if keyent.cget('show') == '*':
            keyent.configure(show='')
            showpas.configure(image=open_eye)
        else:
            keyent.configure(show='*')
            showpas.configure(image=closed_eye)

def help_screen():
     helpscrn = ctk.CTk()
     helpscrn.geometry("400x400")
     helpscrn.mainloop()

def login():
    username = userent.get()
    password = keyent.get()
    if username == "Ojas":
        if password == "blackopal":
            CTkMessagebox(title='Log in successful', message= 'Hello Ojas')
    else:
         CTkMessagebox(title="ERROR",message="USER AND KEY ARE INCORRECT OR USER DOESNT EXIST", icon="cancel")
    
def themed():
    if themeswitch.get() == 0:
        ctk.set_appearance_mode("Dark")
        themeswitch.configure(text="🌙")
    if themeswitch.get() == 1:
        ctk.set_appearance_mode("Light")
        themeswitch.configure(text="☀️")

userlbl = ctk.CTkLabel(app, text="USR:",font=("Arial",20,"bold"))
userlbl.place(x=500,y=300)

userent = ctk.CTkEntry(app, placeholder_text="AAA0001",font=("Arial",20,"bold"))
userent.place(x=580,y=300)
keylbl = ctk.CTkLabel(app, text="KEY:",font=("Arial",20,"bold"))
keylbl.place(x=500,y=400)

keyent = ctk.CTkEntry(app, show="*", placeholder_text="********",font=("Arial",20,"bold"))
keyent.place(x=580,y=400)
keyent.bind("<Return>", lambda e: login())


loginbtn = ctk.CTkButton(app, text="Login",font=("Arial",20,"bold"),command=login)
loginbtn.place(x=550,y=480)


open_eye = ctk.CTkImage(Image.open("eye_open.png"))
closed_eye = ctk.CTkImage(Image.open("eye_closed.png"))
showpas = ctk.CTkButton(master=app,text="",width=5,image=closed_eye, command=show_pass)
showpas.place(x=720,y=402)

info = ctk.CTkImage(Image.open("info_help_icon.png"))
helpbtn = ctk.CTkButton(master=app,text="",width=20,image=info, command=help_screen, compound="top", fg_color="#18445a",bg_color="#18445a")
helpbtn.place(x=1208,y=10)

themeswitch = ctk.CTkSwitch(app,text="🌙",command=themed)
themeswitch.place(x=10,y=770)

app.mainloop()


