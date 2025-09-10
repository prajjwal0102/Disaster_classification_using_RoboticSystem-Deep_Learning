# GUI_main.py (no change needed but included for clarity)
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as ms
import cv2
import os
import numpy as np
from tkvideo import tkvideo

def reg():
    from subprocess import call
    call(["python", "registration.py"])

def log():
    from subprocess import call
    call(["python", "login.py"])

def window():
    root.destroy()

root = tk.Tk()
root.configure(background="brown")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Disaster Classification using Deep Learning")

video_label = tk.Label(root)
video_label.pack()
player = tkvideo("B.mp4", video_label, loop=1, size=(w, h))
player.play()

label_l1 = tk.Label(root, text="Disaster Classification using Deep Learning", font=("Times New Roman", 30, 'bold underline'), background="#152238", fg="white", width=70, height=1)
label_l1.place(x=0, y=0)

button1 = tk.Button(root, text="Login", command=log, width=14, height=1, font=('times', 20, ' bold '), bg="white", fg="black")
button1.place(x=100, y=160)

button2 = tk.Button(root, text="Registeration", command=reg, width=14, height=1, font=('times', 20, ' bold '), bg="white", fg="black")
button2.place(x=100, y=240)

button3 = tk.Button(root, text="Exit", command=window, width=11, height=1, font=('times', 20, ' bold '), bg="#152238", fg="white")
button3.place(x=120, y=320)

root.mainloop()


# login.py (updated to launch dashboard_stream2.py instead of GUI_Master_old.py)
import tkinter as tk
from tkinter import messagebox as ms
import sqlite3

root = tk.Tk()
root.configure(background="white")
root.geometry("700x650+200+50")
root.title("Login Form")

username = tk.StringVar()
password = tk.StringVar()

def registration():
    from subprocess import call
    call(["python", "registration.py"])
    root.destroy()

def login():
    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS admin_registration (Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, Gender TEXT, age TEXT , password TEXT)")
        db.commit()
        find_entry = ('SELECT * FROM admin_registration WHERE username = ? and password = ?')
        c.execute(find_entry, [(username.get()), (password.get())])
        result = c.fetchall()
        if result:
            ms.showinfo("messege", "LogIn successfully")
            root.destroy()
            from subprocess import call
            call(['python', 'dashboard_stream2.py'])  # <- Updated link here
        else:
            ms.showerror('Oops!', 'Username Or Password Did Not Match.')

title = tk.Label(root, text="Login into System", font=("Algerian", 30, "bold", "italic"), bd=5, bg="white", fg="blue")
title.place(x=130, y=150, width=450)

Login_frame = tk.Frame(root, bg="white")
Login_frame.place(x=100, y=200)

lbluser = tk.Label(Login_frame, text="Username", font=("Times new roman", 20, "bold"), bg="white")
lbluser.grid(row=1, column=0, padx=20, pady=10)
txtuser = tk.Entry(Login_frame, bd=5, textvariable=username, font=("", 15))
txtuser.grid(row=1, column=1, padx=20)

lblpass = tk.Label(Login_frame, text="Password", font=("Times new roman", 20, "bold"), bg="white")
lblpass.grid(row=2, column=0, padx=50, pady=10)
txtpass = tk.Entry(Login_frame, bd=5, textvariable=password, show="*", font=("", 15))
txtpass.grid(row=2, column=1, padx=20)

btn_log = tk.Button(Login_frame, text="Login", command=login, width=15, font=("Times new roman", 14, "bold"), bg="Green", fg="white")
btn_log.grid(row=3, column=1, pady=10)
btn_reg = tk.Button(Login_frame, text="Sign Up", command=registration, width=15, font=("Times new roman", 14, "bold"), bg="red", fg="white")
btn_reg.grid(row=3, column=0, pady=10)

root.mainloop()


# registration.py (no changes needed; already returns to login)
# dashboard_stream2.py (no changes needed; already includes SETTINGS, EXIT, etc.)
