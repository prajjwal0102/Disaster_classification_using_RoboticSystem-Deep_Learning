# object_detector.py

from ultralytics import YOLO
import cv2
from PIL import Image, ImageTk

# Load the YOLO model once (you can switch to yolov8s.pt or yolov8m.pt for better accuracy)
model = YOLO("yolov8n.pt")


def detect_from_stream(cap, label_widget, stop_flag_func):
    """
    Runs YOLO detection on frames from a video stream and updates the given Tkinter label with annotated images.
    
    Args:
        cap (cv2.VideoCapture): OpenCV video capture object.
        label_widget (tk.Label): Tkinter label to update with annotated frames.
        stop_flag_func (function): Function that returns True when streaming should stop.
    """
    while not stop_flag_func():
        ret, frame = cap.read()
        if not ret:
            continue

        # Run YOLOv8 detection
        results = model(frame)

        # Plot annotated results
        annotated_frame = results[0].plot()

        # Resize for display
        frame_resized = cv2.resize(annotated_frame, (400, 350))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        # Update GUI label with new image
        label_widget.configure(image=img_tk)
        label_widget.image = img_tk
        label_widget.update_idletasks()

    cap.release()
