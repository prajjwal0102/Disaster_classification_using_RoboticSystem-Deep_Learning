import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import time
from datetime import datetime
from tensorflow.keras.models import load_model
import pywhatkit
import CNNModel
#from ultralytics import YOLO
from subprocess import call

# Disable OneDNN warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Load model
if os.path.exists("D_model.h5"):
    model = load_model("D_model.h5")
else:
    model = None
    
#load Yolov8
#yolo_model = YOLO("yolov8n.pt") #yolovv8s.pt for more accuracy

# Snapshot folder
if not os.path.exists("snapshots"):
    os.makedirs("snapshots")

# Global variables
stream_url = "http://192.168.16.47:81/stream"
cap = None
streaming = False
current_frame = None

selected_pil_image = None

# GUI-------------------------------------------------------------------
root = tk.Tk()
root.title("Disaster Classification System Dashboard")
root.configure(bg='black')
root.geometry("1200x700")

PHONE_NUMBER = "+917028902209"
label_result = None
result_box_label = None

# ================= FUNCTION DEFINITIONS =================

def start_stream():
    global cap, streaming
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Failed to open stream.")
        return
    streaming = True
    update_frame()

def stop_stream():
    global cap, streaming
    streaming = False
    if cap:
        cap.release()
    live_image_label.configure(image='')

def toggle_stream():
    if streaming:
        stop_stream()
        stream_toggle_btn.config(text="Start Feed", bg="green")
    else:
        start_stream()
        stream_toggle_btn.config(text="Stop Feed", bg="red")

def update_frame():
    global current_frame, cap
    if streaming and cap:
        ret, frame = cap.read()
        if ret:
            current_frame = frame
            
            #run yolo
 #           results = yolo_model(frame)
 #           annotated_frame = results[0].plot()
            
            #resize and convert display
            resized = cv2.resize(frame, (600, 400))
            rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(rgb_image))
            live_image_label.imgtk = imgtk
            live_image_label.configure(image=imgtk)
        live_image_label.after(15, update_frame)

def capture_image():
    global current_frame
    if current_frame is not None:
        img = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
        filename = f"snapshots/snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        img.save(filename)
        messagebox.showinfo("Captured", f"Saved: {filename}")
    else:
        messagebox.showerror("Capture Error", "No frame to capture.")

def image_selection():
    global selected_pil_image
    file_path = filedialog.askopenfilename(title="Select an Image",
                                           filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        try:
            selected_pil_image = Image.open(file_path)
            display_image = selected_pil_image.resize((400, 350))
            img_tk = ImageTk.PhotoImage(display_image)
            image_placeholder_labels[0].configure(image=img_tk, text="")
            image_placeholder_labels[0].image = img_tk
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image.\n{e}")

def pre_processing():
    global selected_pil_image
    if selected_pil_image is None:
        messagebox.showerror("Pre-Processing Error", "Please select an image first.")
        return
    try:
        open_cv_image = np.array(selected_pil_image.convert("RGB"))
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
        img_resized = cv2.resize(open_cv_image, (300, 300))
        gray_img = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        _, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
        img_tk_gray = ImageTk.PhotoImage(Image.fromarray(gray_img))
        img_tk_binary = ImageTk.PhotoImage(Image.fromarray(binary_img))
        image_placeholder_labels[1].configure(image=img_tk_gray, text="")
        image_placeholder_labels[1].image = img_tk_gray
        image_placeholder_labels[2].configure(image=img_tk_binary, text="")
        image_placeholder_labels[2].image = img_tk_binary
        messagebox.showinfo("Pre-processing", "Completed successfully!")
    except Exception as e:
        messagebox.showerror("Processing Error", f"{e}")

def update_label1(str_T):
    global label_result
    if label_result:
        label_result.destroy()
    label_result = tk.Label(root, text=str_T, width=60, font=("bold", 18), bg='white', fg='black')
    label_result.place(x=300, y=650)

def train_model():
    update_label1("Model Training Started. Please wait...")
    root.update()
    start = time.time()
    result = CNNModel.main()
    end = time.time()
    msg = f"{result}\nExecution Time: {end - start:.2f} sec"
    update_label1(msg)
    messagebox.showinfo("Training Status", msg)

def test():
    global selected_pil_image, model, result_box_label
    if selected_pil_image is None:
        messagebox.showerror("Test Error", "Please select an image.")
        return
    if model is None:
        messagebox.showerror("Model Error", "Model not loaded.")
        return

    update_label1("Processing, please wait...")
    root.update()

    def do_prediction():
        try:
            img = selected_pil_image.resize((64, 64))
            img_array = np.array(img) / 255.0
            if img_array.shape[-1] == 4:
                img_array = img_array[:, :, :3]
            img_array = np.expand_dims(img_array, axis=0)
            prediction = model.predict(img_array)[0]
            classes = ['Earthquake','Fire', 'Flood', 'Landslide',"Human_Damage","Non-Damage Buildings/Streets"]
            predicted_class = classes[np.argmax(prediction)]
            confidence = np.max(prediction) * 100
            result = f"Prediction: {predicted_class} ({confidence:.2f}%)"
            update_label1(result)
            result_box_label.config(text=result)
            messagebox.showinfo("Result", result)
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

    root.after(2000, do_prediction)
    
def graph():
    try:
        image_path = r"C:\Users\prajj\OneDrive\Desktop\object detection\accuracy.png"

        if not os.path.exists(image_path):
            messagebox.showerror("Graph Error", f"Image not found at:\n{image_path}")
            return

        # Open new window
        graph_win = tk.Toplevel(root)
        graph_win.title("Training Graph")
        graph_win.geometry("850x650")

        # Load and resize image
        img = Image.open(image_path)
        img = img.resize((800, 600), Image.LANCZOS)  # Use LANCZOS instead of deprecated ANTIALIAS
        img_tk = ImageTk.PhotoImage(img)

        # Label to show image
        label = tk.Label(graph_win, image=img_tk)
        label.image = img_tk  # prevent garbage collection
        label.pack(padx=20, pady=20)

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(error_details)  # Print to terminal
        messagebox.showerror("Graph Display Error", f"{str(e)}\n\nDetails:\n{error_details}")




def setting():
    def save_settings():
        nonlocal phone_var, stream_url_var
        global PHONE_NUMBER, stream_url

        new_phone = phone_var.get().strip()
        new_stream = stream_url_var.get().strip()

        if not new_phone.startswith("+") or len(new_phone) < 10:
            messagebox.showerror("Invalid Phone", "Use +91... format")
            return
        if not (new_stream.startswith("http://") or new_stream.startswith("https://")):
            messagebox.showerror("Invalid URL", "Use valid HTTP stream URL")
            return

        PHONE_NUMBER = new_phone
        stream_url = new_stream
        messagebox.showinfo("Saved", "Settings updated")
        settings_win.destroy()

    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("400x220")
    settings_win.configure(bg="lightgray")
    settings_win.resizable(False, False)

    tk.Label(settings_win, text="WhatsApp Number:", bg="lightgray").pack(pady=(20, 5))
    phone_var = tk.StringVar(value=PHONE_NUMBER)
    tk.Entry(settings_win, textvariable=phone_var, width=30).pack()

    tk.Label(settings_win, text="Stream URL:", bg="lightgray").pack(pady=(10, 5))
    stream_url_var = tk.StringVar(value=stream_url)
    tk.Entry(settings_win, textvariable=stream_url_var, width=30).pack()

    tk.Button(settings_win, text="Save", command=save_settings,
              bg="green", fg="white").pack(pady=20)

def alert_responder(responder):
    try:
        msg = f"🚨 Emergency Alert! Please dispatch {responder} to the location."
        pywhatkit.sendwhatmsg_instantly(PHONE_NUMBER, msg, wait_time=10, tab_close=True)
        messagebox.showinfo("Alert Sent", f"{responder} alerted.")
    except Exception as e:
        messagebox.showerror("WhatsApp Error", str(e))



def exit_application():
    global cap, streaming
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        streaming = False
        if cap:
            cap.release()
        root.destroy()
        call(["python", "login.py"])

# ================= GUI LAYOUT =================

tk.Label(root, text="DISASTER CLASSIFICATION SYSTEM", bg='black', fg='gray', font=("Arial", 10)).pack(fill=tk.X)
tk.Label(root, text="DASHBOARD", bg='white', fg='black', font=("Arial", 20, "bold")).pack(fill=tk.X, pady=10)

main_frame = tk.Frame(root, bg='black')
main_frame.pack(fill=tk.BOTH, expand=True)

menu_frame = tk.Frame(main_frame, bg='black')
menu_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)

menu_buttons = [
    ("IMAGE SELECTION", image_selection),
    ("PRE PROCESSING", pre_processing),
    ("TRAIN", train_model),
    ("TEST", test),
    ("GRAPH",graph),
    ("SETTING", setting),
    ("LOGOUT", exit_application)
]

for text, cmd in menu_buttons:
    tk.Button(menu_frame, text=text, command=cmd, bg='gray', fg='white',
              font=("Arial", 10), relief=tk.FLAT).pack(fill=tk.X, pady=2, padx=2)

live_feed_frame = tk.Frame(main_frame, bg='gray', bd=2, relief=tk.SOLID)
live_feed_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

tk.Label(live_feed_frame, text="LIVE FEED FROM CAMERA", bg='gray', fg='white', font=("Arial", 14)).pack(pady=5)

live_image_label = tk.Label(live_feed_frame, bg='black')
live_image_label.pack(padx=5, pady=5)

button_control_frame = tk.Frame(live_feed_frame, bg='gray')
button_control_frame.pack(pady=(0, 10))

stream_toggle_btn = tk.Button(button_control_frame, text="Start Feed", command=toggle_stream,
                              bg='green', fg='black', font=("Arial", 9, "bold"), width=12)
stream_toggle_btn.pack(side=tk.LEFT, padx=5)

tk.Button(button_control_frame, text="Capture", command=capture_image,
          bg='red', fg='white', font=("Arial", 9, "bold"), width=12).pack(side=tk.LEFT, padx=5)

alert_responder_frame = tk.Frame(main_frame, bg='black')
alert_responder_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

alert_frame = tk.Frame(alert_responder_frame, bg='gray', bd=2, relief=tk.SOLID)
alert_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

def create_centered_label(parent, text, font, fg, bg, padding):
    frame = tk.Frame(parent, bg=bg)
    frame.pack(fill=tk.X, pady=padding)
    label = tk.Label(frame, text=text, bg=bg, fg=fg, font=font)
    label.pack(expand=True, padx=padding)
    return label

create_centered_label(alert_frame, "ALERT", ("Arial", 16, "bold"), "red", "gray", 10)
create_centered_label(alert_frame, "DISASTER TYPE", ("Arial", 10), "red", "gray", 10)
create_centered_label(alert_frame, "RESULT", ("Arial", 10), "green", "gray", 10)

result_box_label = tk.Label(alert_frame, text="", bg='white', fg='black',
                            font=("Arial", 10), relief=tk.SOLID, width=40, height=2)
result_box_label.pack(pady=5)

responder_frame = tk.Frame(alert_responder_frame, bg='gray', bd=2, relief=tk.SOLID)
responder_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(responder_frame, text="RESPONDER ALERTS", bg='gray', fg='white', font=("Arial", 10)).pack(anchor='w', padx=5, pady=5)

responder_buttons = ["AMBULANCE", "FIRE BRIGADE", "POLICE", "NDMA"]
for responder in responder_buttons:
    tk.Button(responder_frame, text=responder,
              command=lambda r=responder: alert_responder(r),
              bg='green', fg='black', font=("Arial", 10), relief=tk.FLAT).pack(fill=tk.X, pady=2, padx=2)

image_frame = tk.Frame(main_frame, bg='gray', bd=2, relief=tk.SOLID)
image_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

image_placeholder_labels = []
for label_text in ["ORIGINAL IMAGE", "GRAY IMAGE", "BINARY IMAGE"]:
    container = tk.Frame(image_frame, bg='white', bd=2, relief=tk.SOLID, width=300, height=300)
    container.pack_propagate(False)
    container.pack(side=tk.LEFT, expand=True, padx=10, pady=10)
    label = tk.Label(container, text=label_text, bg='lightgray', font=("Arial", 12), width=30, height=15)
    label.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
    image_placeholder_labels.append(label)

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=0)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=2)
main_frame.grid_columnconfigure(2, weight=1)

root.mainloop()