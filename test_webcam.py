# test_webcam.py

from ultralytics import YOLO
import cv2

# Load model
model = YOLO("yolov8n.pt")

# Open webcam (0 is default webcam index)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform detection
    results = model(frame)

    # Plot results
    annotated_frame = results[0].plot()

    # Show frame
    cv2.imshow("YOLOv8 Webcam Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()












