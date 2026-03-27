🏥 AI-Based Patient Monitoring & Fall Detection System
🚨 Overview
This project is an AI-powered patient monitoring system designed for healthcare environments such as hospitals, elderly care centers, and home care setups. It uses computer vision (YOLOv8) to continuously monitor patients and detect posture changes and fall events in real-time.

The system helps reduce dependency on manual supervision and ensures immediate alerts during critical situations like falls, improving patient safety.

🎯 Problem Statement
Falls among elderly or physically weak patients can lead to severe injuries if not detected quickly.

❌ Existing Challenges:
Requires continuous human supervision

Delayed response to fall incidents

No automated monitoring system

✅ Our Solution:
Real-time posture detection (Standing, Sitting, Lying)

Instant fall detection using AI

Live monitoring through video feed

Automated alerts (sound + voice)

🚀 Features
🧠 AI-Based Detection
Uses YOLOv8 for person detection

Detects posture based on bounding box ratio

Identifies sudden falls using motion + posture transition

📊 Real-Time Monitoring
Live video processing

Continuous posture tracking

Displays patient status in real-time

🚨 Smart Fall Detection
Detects fall using:

Standing → Lying transition

Sitting → Lying transition

Sudden vertical drop

🔔 Alert System
🔊 Beep sound alert

🗣 Voice alert: “Fall detected”

Real-time visual alert on screen

🖥️ Interactive Dashboard (Tkinter UI)
Patient selection panel

Multiple patient support

Clean, user-friendly interface

Centered layout with medical-themed design

📌 On-Screen Information Panel
Displays:

Patient Name

Patient ID

Current Status (Standing / Sitting / Lying / FALL DETECTED)

Real-time clock

🛠️ Tech Stack
Language: Python

Computer Vision: OpenCV

AI Model: YOLOv8

GUI: Tkinter

Audio Alerts: pyttsx3, winsound

📁 Project Structure
patient_monitoring/
│
├── main.py
├── yolov8s.pt
├── video1.mp4
├── video2.mp4
├── video3.mp4
├── fall_log.txt
└── assets/
▶️ How to Run
1️⃣ Clone the repository
git clone https://github.com/your-username/patient-monitoring-system.git
cd patient-monitoring-system
2️⃣ Install dependencies
pip install ultralytics opencv-python pyttsx3 pillow
3️⃣ Run the project
python main.py
🖥️ How It Works
Launch the application

Select a patient from the dashboard

Video feed starts

System detects posture in real-time

If fall is detected:

Alert sound + voice triggers

Status changes to FALL DETECTED

🧠 Core Logic
Posture Detection:
Height / Width ratio of bounding box
1.1 → Standing

0.75 – 1.1 → Sitting

< 0.75 → Lying

Fall Detection:
Lying posture + sudden transition OR sudden drop
📸 Output Example
Real-time video with bounding box

Top-left info panel

Status updates dynamically

🎓 Use Cases
Hospitals 🏥

Elderly care homes 👵

Home healthcare 🏠

Rehabilitation centers

🚀 Future Enhancements
📊 Dashboard analytics

📱 Mobile notifications

🧍 Pose estimation for accuracy

☁️ Cloud-based monitoring

🧑‍⚕️ Multi-patient live tracking
