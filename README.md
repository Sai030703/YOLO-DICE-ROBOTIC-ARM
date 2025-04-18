# YOLO-DICE-ROBOTIC-ARM

YOLOv11 Dice Detection & Robotic Arm Control
🎯 A computer vision + robotics integration project using a YOLOv11 model to detect dice values in real time and control an Igus robotic arm, first in simulation via Igus IRC (Digital Twin), then on real hardware.


# 🔧 Technologies Used

* YOLOv11 (Ultralytics)
* Python
* OpenCV
* Roboflow (for annotation and dataset generation)
* TCP/IP socket programming
* Igus Robotic Arm
* Igus IRC Digital Twin Environment

# 🧠 Project Workflow

* 📸 Images of dice were annotated in Roboflow
* 🧠 A YOLOv11 model was trained and tested
* 🎥 Real-time detection using webcam and OpenCV
* 🤖 The detected number is used to trigger robotic arm movements via CRI commands
* 🧪 Simulated first using Igus IRC (digital twin)


# ⚙️ Files Explained

* main.py – Real-time YOLO detection + task dispatch
* robot_controller.py – TCP/IP control interface for Igus robot
* my_model.pt – YOLOv11 model trained on dice detection

# Sample Output – Real-Time Dice Detection 

This image shows a successful inference result using the custom-trained YOLOv11 model on a webcam frame. The model detects two sides of a dice:
* Class 6 with 87% confidence (top face)
* Class 5 with 63% confidence (front face)
  
![output](https://github.com/user-attachments/assets/0bdedb35-37e2-45d1-8919-05a18a0c6039)



