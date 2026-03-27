from ultralytics import YOLO
import cv2
from datetime import datetime
import pyttsx3
import winsound
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# -------------------------------
# PATIENT DATABASE
# -------------------------------
patients = {
    "001": {"name": "Sofia", "video": "video1.mp4"},
    "002": {"name": "John", "video": "video2.mp4"},
    "003": {"name": "Mack", "video": "video3.mp4"}
}

# -------------------------------
# MONITORING FUNCTION
# -------------------------------
def start_monitoring(patient_id):
    PATIENT_NAME = patients[patient_id]["name"]
    video_path = patients[patient_id]["video"]

    engine = pyttsx3.init()
    model = YOLO("yolov8s.pt")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        messagebox.showerror("Error", "Video not found")
        return

    previous_posture = "Unknown"
    fall_confirmed = False
    prev_y = None

    while True:
        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.resize(frame, (1200, 800))
        results = model(frame, conf=0.3)

        posture = "Unknown"
        sudden_drop = False

        for result in results:
            for box in result.boxes:
                if int(box.cls[0]) == 0:
                    x1, y1, x2, y2 = box.xyxy[0]

                    width = x2 - x1
                    height = y2 - y1
                    ratio = height / width

                    if ratio > 1.1:
                        posture = "Standing"
                    elif ratio > 0.75:
                        posture = "Sitting"
                    else:
                        posture = "Lying"

                    y_center = (y1 + y2) / 2
                    if prev_y is not None and abs(y_center - prev_y) > 50:
                        sudden_drop = True
                    prev_y = y_center

                    color = (0, 0, 255) if fall_confirmed else (0, 255, 0)

                    cv2.rectangle(frame, (int(x1), int(y1)),
                                  (int(x2), int(y2)), color, 3)

        # -------------------------------
        # FALL DETECTION
        # -------------------------------
        if posture == "Lying" and (previous_posture in ["Standing", "Sitting"] or sudden_drop):
            fall_confirmed = True

        if posture in ["Standing", "Sitting"]:
            fall_confirmed = False

        previous_posture = posture

        # -------------------------------
        # ALERT
        # -------------------------------
        if fall_confirmed:
            winsound.Beep(1500, 500)
            engine.say("Fall detected")
            engine.runAndWait()

        # -------------------------------
        # 🔥 TOP LEFT PANEL (REAL-TIME)
        # -------------------------------
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (380, 170), (20, 20, 20), -1)
        frame = cv2.addWeighted(overlay, 0.75, frame, 0.25, 0)

        current_time = datetime.now().strftime("%H:%M:%S")

        # Name
        cv2.putText(frame, f"Patient: {PATIENT_NAME}", (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # ID
        cv2.putText(frame, f"ID: {patient_id}", (15, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Status
        if fall_confirmed:
            status_text = "FALL DETECTED"
            status_color = (0, 0, 255)
        elif posture == "Standing":
            status_text = "Standing"
            status_color = (0, 255, 0)
        elif posture == "Sitting":
            status_text = "Sitting"
            status_color = (0, 255, 255)
        elif posture == "Lying":
            status_text = "Lying"
            status_color = (255, 255, 0)
        else:
            status_text = "Detecting..."
            status_color = (200, 200, 200)

        cv2.putText(frame, f"Status: {status_text}", (15, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, status_color, 2)

        # Time
        cv2.putText(frame, f"Time: {current_time}", (15, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # -------------------------------
        # DISPLAY
        # -------------------------------
        cv2.imshow("Monitoring", frame)

        if cv2.getWindowProperty("Monitoring", cv2.WND_PROP_VISIBLE) < 1:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# -------------------------------
# MAIN UI
# -------------------------------
root = tk.Tk()
root.title("AI Patient Monitoring Dashboard")
root.geometry("700x450")
root.configure(bg="#f8c8dc")

# HEADER
tk.Label(root, text="Patient Monitoring System",
         font=("Arial", 18, "bold"),
         bg="#f8c8dc").pack(pady=10)

# MAIN FRAME
main_frame = tk.Frame(root, bg="#f8c8dc")
main_frame.pack(fill="both", expand=True)

# LEFT PANEL
left = tk.Frame(main_frame, bg="#ffffff", width=200)
left.pack(side="left", fill="y", padx=10, pady=10)

tk.Label(left, text="Patients", font=("Arial", 14, "bold"),
         bg="white").pack(pady=10)

for pid, info in patients.items():
    tk.Button(left,
              text=f"{info['name']} ({pid})",
              command=lambda p=pid: start_monitoring(p),
              bg="#ff69b4",
              fg="white",
              font=("Arial", 11),
              relief="flat").pack(pady=5, fill="x")

# RIGHT PANEL
right = tk.Frame(main_frame, bg="#f8c8dc")
right.pack(side="right", fill="both", expand=True)

# IMAGE
img_path = r"C:\Users\jasmi\OneDrive\Desktop\360_F_96481179_ANEpnLLHZZxtIezAh5k3tTKHO3VaFqjF.jpg"
img = Image.open(img_path)
img = img.resize((150, 150))
img = ImageTk.PhotoImage(img)

# CENTER
center_frame = tk.Frame(right, bg="#f8c8dc")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(center_frame, image=img, bg="#f8c8dc").pack(pady=10)

tk.Label(center_frame,
         text="Select a patient to start monitoring",
         font=("Arial", 12, "bold"),
         bg="#f8c8dc").pack()

# FOOTER
tk.Label(root, text="Press 'q' to stop monitoring",
         bg="#f8c8dc", font=("Arial", 10)).pack(pady=5)

root.mainloop()