import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import re
from subprocess import call

window = tk.Tk()
window.geometry("700x700")
window.title("REGISTRATION FORM")
window.configure(background="white")

Fullname = tk.StringVar()
address = tk.StringVar()
username = tk.StringVar()
Email = tk.StringVar()
Phoneno = tk.IntVar()
var = tk.IntVar()
age = tk.IntVar()
password = tk.StringVar()
password1 = tk.StringVar()

# Database setup
db = sqlite3.connect('evaluation.db')
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_registration (
        Fullname TEXT, address TEXT, username TEXT, Email TEXT,
        Phoneno TEXT, Gender TEXT, age TEXT, password TEXT
    )
""")
db.commit()

def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True
    if len(passwd) < 6 or len(passwd) > 20:
        val = False
    if not any(char.isdigit() for char in passwd):
        val = False
    if not any(char.isupper() for char in passwd):
        val = False
    if not any(char.islower() for char in passwd):
        val = False
    if not any(char in SpecialSym for char in passwd):
        val = False
    return val

def insert():
    fname, addr, un, email = Fullname.get(), address.get(), username.get(), Email.get()
    mobile, gender, time = Phoneno.get(), var.get(), age.get()
    pwd, cnpwd = password.get(), password1.get()

    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()
        c.execute('SELECT * FROM admin_registration WHERE username = ?', [(un)])
        user_exists = c.fetchall()

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    valid_email = re.search(regex, email)

    if fname.isdigit() or fname == "":
        ms.showerror("Error", "Please enter valid name")
    elif addr == "":
        ms.showerror("Error", "Please enter address")
    elif not email or not valid_email:
        ms.showerror("Error", "Please enter a valid email")
    elif len(str(mobile)) != 10:
        ms.showerror("Error", "Please enter 10-digit mobile number")
    elif time <= 0 or time > 100:
        ms.showerror("Error", "Please enter valid age")
    elif user_exists:
        ms.showerror('Error!', 'Username already exists')
    elif not password_check(pwd):
        ms.showerror("Error", "Password must contain 1 uppercase, 1 number, 1 symbol")
    elif pwd != cnpwd:
        ms.showerror("Error", "Passwords do not match")
    else:
        conn = sqlite3.connect('evaluation.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO admin_registration VALUES (?,?,?,?,?,?,?,?)',
                           (fname, addr, un, email, mobile, gender, time, pwd))
            conn.commit()
        ms.showinfo('Success', 'Account Created Successfully')
        window.destroy()
        call(["python", "login.py"])

# GUI Labels and Entries
l1 = tk.Label(window, text="Create Your Account Here!!", font=("Times new roman", 30, "bold"), bg="white")
l1.place(x=120, y=50)

labels = ["Full Name", "Address", "E-mail", "Phone number", "Gender", "Age", "User Name", "Password", "Confirm Password"]
variables = [Fullname, address, Email, Phoneno, var, age, username, password, password1]
y_positions = [150, 200, 250, 300, 350, 400, 450, 500, 550]

for i, label in enumerate(labels):
    if label == "Gender":
        tk.Label(window, text=label+" :", width=12, font=("Times new roman", 15, "bold"), bg="snow").place(x=130, y=y_positions[i])
        tk.Radiobutton(window, text="Male", variable=var, value=1, font=("bold", 15), bg="snow").place(x=330, y=350)
        tk.Radiobutton(window, text="Female", variable=var, value=2, font=("bold", 15), bg="snow").place(x=440, y=350)
    else:
        tk.Label(window, text=label+" :", width=12, font=("Times new roman", 15, "bold"), bg="snow").place(x=130, y=y_positions[i])
        show = "*" if "Password" in label else ""
        tk.Entry(window, textvariable=variables[i], font=("", 15), show=show).place(x=330, y=y_positions[i])

btn = tk.Button(window, text="Register", bg="green", font=("", 20), fg="white", command=insert)
btn.place(x=250, y=600)

window.mainloop()
