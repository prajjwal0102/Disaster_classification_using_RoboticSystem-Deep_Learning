

import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as ms
import cv2
import sqlite3
import os
import numpy as np
import time
from tkvideo import tkvideo


global fn
fn = ""
##############################################+=============================================================
root = tk.Tk()
root.configure(background="black")
# root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Disaster Classification using Deep Learning")
#video_label =tk.Label(root)
#video_label.pack()
#read video to display on label
#player = tkvideo("B.mp4", video_label,loop = 1, size = (w, h))
#player.play()

# 43

# ++++++++++++++++++++++++++++++++++++++++++++
# #####For background Image
image2 = Image.open('accuracy.png')
image2 = image2.resize((1230, 700))

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)
background_label.image = background_image

background_label.place(x=200, y=50)  # , relwidth=1, relheight=1)

# img=ImageTk.PhotoImage(Image.open("s1.jpg"))

# img2=ImageTk.PhotoImage(Image.open("s2.jpg"))

# img3=ImageTk.PhotoImage(Image.open("s3.jpg"))


# logo_label=tk.Label()
# logo_label.place(x=0,y=100)

# x = 1

# # function to change to next image
# def move():
# 	global x
# 	if x == 4:
# 		x = 1
# 	if x == 1:
# 		logo_label.config(image=img)
# 	elif x == 2:
# 		logo_label.config(image=img2)
# 	elif x == 3:
# 		logo_label.config(image=img3)
# 	x = x+1
# 	root.after(2000, move)

# # calling the function
# move()



#
label_l1 = tk.Label(root, text="Disaster Classification using Deep Learning",font=("Times New Roman", 30, 'bold underline'),
                    background="#152238", fg="white", width=70, height=1)
label_l1.place(x=0, y=0)

#T1.tag_configure("center", justify='center')
#T1.tag_add("center", 1.0, "end")

################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#def clear_img():
#    img11 = tk.Label(root, background='bisque2')
#    img11.place(x=0, y=0)


#################################################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# def cap_video():
    
#     video1.upload()
#     #from subprocess import call
#     #call(['python','video_second.py'])



root.mainloop()