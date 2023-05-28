# import necessary modules
from tkinter import *
from tkinter.ttk import Progressbar, Combobox, Notebook, Treeview
from PIL import Image, ImageTk
import tkinter.font
import tkinter.messagebox
import customtkinter

def login():
    #login logic import
    auth_successful = True
    if auth_successful:
        print("W")
        loading.stop()
        loading.destroy()
        login_button.configure(state="normal")
        if LoginTab.index("end") >= 2:  # check if there are at least 3 tabs
            ta2_state = "normal"  # enable C2 tab
            ta3_state = "normal"  # enable Man Page tab
            LoginTab.tab(0, state=ta2_state)
            LoginTab.tab(1, state=ta3_state)
        return "Auth Successful"
    else:
        loading.stop()
        loading.destroy()
        login_button.configure(state="normal")
        return "Auth Failed"


# set appearance mode and default color theme for customtkinter
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

# create main window
w1 = Tk()
w1.configure(bg='#000000')
w1.geometry('1270x800')
w1.title("BlackOpal")

# create notebook for tabs
LoginTab = Notebook(w1)
LoginTab.place(x=0, y=0, width=1270, height=800)

# create login tab
ta1 = Frame(LoginTab)
ta1.place(x=0, y=0, width=1266, height=771)

# create banner
banner = customtkinter.CTkCanvas(ta1, bg='white', width=1270, height=250)
banner.place(x=-2, y=-4)
banneri = Image.open("C:/Users/cyn0v/Desktop/pfp/banner.png")
bannerimg = ImageTk.PhotoImage(banneri.resize((1270, 250)))
banner.create_image(0, 0, image=bannerimg, anchor=NW)

# create question button
help_img = customtkinter.CTkImage(Image.open("C:/Users/cyn0v/Desktop/pfp/question everything.png"), size=(20, 20))
help_button = customtkinter.CTkButton(ta1, text="", fg_color="#13262d", font=("Calibri", 9), cursor="arrow", state="normal", image=help_img, compound="top", width=20, height=20)
help_button.place(x=1230, y=-2)

# create username and key entries
usr_entry = customtkinter.CTkEntry(ta1, text_color="#976bef", font=("Dubai", 20), state="normal", width=150, height=32)
usr_entry.place(x=610, y=356)
key_entry = customtkinter.CTkEntry(ta1, text_color="#976bef", font=("Dubai", 20), state="normal", width=150, height=32)
key_entry.place(x=610, y=410)

# create username and key labels
key_lbl = customtkinter.CTkLabel(ta1, text="KEY:", anchor='w', text_color="#05c0a1", font=("digital display tfb", 28), cursor="arrow", state="normal", width=80, height=32)
key_lbl.place(x=530, y=410)
usr_lbl = customtkinter.CTkLabel(ta1, text="USR:", anchor='w', text_color="#05c0a1", font=("digital display tfb", 28), cursor="arrow", state="normal", width=80, height=32)
usr_lbl.place(x=530, y=356)

# create loading bar
loading = customtkinter.CTkProgressBar(ta1, cursor="arrow", width=230, height=10)
loading.place(x=528, y=446)
loading['value'] = 0

# create login button
login_button = customtkinter.CTkButton(ta1, text="Login", fg_color="#5bc0d2", text_color="#000000", font=("digital display tfb", 28), cursor="arrow", state="normal", width=230, height=42, command=login)
login_button.place(x=528, y=476)

# create C2 tab
ta2 = Frame(LoginTab)
ta2.place(x=0, y=0, width=1266, height=771)
ta2_state = "disabled"  # set initial state to disabled

# add C2 tab to notebook
LoginTab.add(ta2, text="C2 | BlackOpal", state=ta2_state)

# create Man Page tab
ta3 = Frame(LoginTab)
ta3.place(x=0, y=0, width=1266, height=771)
ta3_state = "disabled"  # set initial state to disabled

# add Man Page tab to notebook
LoginTab.add(ta3, text="Man Page | BlackOpal", state=ta3_state)

# run main window
w1.mainloop()