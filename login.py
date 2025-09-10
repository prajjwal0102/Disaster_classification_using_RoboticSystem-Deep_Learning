import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
from subprocess import call

# Window setup
root = tk.Tk()
root.configure(background="white")
root.geometry("700x650+200+50")
root.title("Login Form")

# Variables
username = tk.StringVar()
password = tk.StringVar()

# Redirect to registration
def registration():
    call(["python", "registration.py"])
    root.destroy()

# Login and redirect to dashboard_stream2.py
def login():
    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()
        c.execute("SELECT * FROM admin_registration WHERE username = ? AND password = ?",
                  (username.get(), password.get()))
        result = c.fetchall()
        if result:
            ms.showinfo("Success", "Login successful!")
            root.destroy()
            call(["python", "dashboard_stream2.py"])
        else:
            ms.showerror("Error", "Invalid Username or Password")

# UI
title = tk.Label(root, text="Login into System", font=("Algerian", 30, "bold", "italic"), bg="white", fg="blue")
title.place(x=130, y=150, width=450)

Login_frame = tk.Frame(root, bg="white")
Login_frame.place(x=100, y=200)

tk.Label(Login_frame, text="Username", font=("Times new roman", 20, "bold"), bg="white").grid(row=1, column=0, padx=20, pady=10)
tk.Entry(Login_frame, textvariable=username, font=("", 15)).grid(row=1, column=1, padx=20)

tk.Label(Login_frame, text="Password", font=("Times new roman", 20, "bold"), bg="white").grid(row=2, column=0, padx=20, pady=10)
tk.Entry(Login_frame, textvariable=password, show="*", font=("", 15)).grid(row=2, column=1, padx=20)

tk.Button(Login_frame, text="Login", command=login, font=("Times new roman", 14, "bold"), bg="green", fg="white").grid(row=3, column=1, pady=10)
tk.Button(Login_frame, text="Sign Up", command=registration, font=("Times new roman", 14, "bold"), bg="red", fg="white").grid(row=3, column=0, pady=10)

root.mainloop()
