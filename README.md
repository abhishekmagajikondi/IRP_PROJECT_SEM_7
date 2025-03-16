# IRP_PROJECT_SEM_7

# Traffic Detection and Count System

This project detects and counts different types of vehicles (bus, car, auto-rickshaw, motorcycle) using YOLO (You Only Look Once) for object detection and transmits the data to an Arduino receiver via ESP-NOW or Serial Communication.

# 📂 Project Structure

```
  ├── sender_arduino.ino       # Arduino sketch for sending data
  ├── reciever_arduino.ino     # Arduino sketch for receiving data
  ├── send_arduino.py          # Python script for YOLO-based vehicle detection
  ├── coco1.txt                # Class labels for YOLO
  ├── best.pt                  # Trained YOLO model (Not included, download separately)
  ├── id4.mp4                  # Video file for object detection
```


# ⚡ Requirements

## 1️⃣ Hardware

ESP8266/ESP32 (for ESP-NOW) OR Arduino with Serial Communication

USB Cable

Camera (Optional, if using live feed)

## 2️⃣ Software & Libraries

Python 3.x installed

Install the required Python libraries:

pip install opencv-python pandas ultralytics cvzone pyserial

Arduino IDE with ESP8266/ESP32 board support (if using ESP-NOW)


# 🚀 Setup & Running Order

## Step 1: Upload Arduino Sketches

Connect the Receiver Arduino and open reciever_arduino.ino in Arduino IDE.

Select the correct board and COM port, then upload the code.

Repeat the same for Sender Arduino, using sender_arduino.ino.

# 📌 Note: Ensure both devices use the same baud rate (115200).

## Step 2: Run YOLO Detection (Python Script)

Ensure best.pt (YOLO model) is present in the project folder.

Run the Python script to start vehicle detection:

python send_arduino.py

The script will process the video and send vehicle counts to Arduino.

## Step 3: Monitor Arduino Serial Output

Open Arduino IDE → Tools → Serial Monitor.

Set baud rate to 115200.

You should see real-time vehicle counts updating.

# 🔧 Troubleshooting

## ✅ Issue: Serial port error

Ensure the correct COM port is set in send_arduino.py:

ser = serial.Serial('COM3', 115200)  # Change 'COM3' if needed

## ✅ Issue: No YOLO model found

Download the trained YOLO model (best.pt) and place it in the same folder.

## ✅ Issue: No data in Arduino Serial Monitor

Check if the Python script is running and sending data.

Ensure the correct baud rate (115200) is set in both send_arduino.py and Arduino sketches.

# 📜 License

This project is open-source. Feel free to modify and use it for personal or research purposes.

# 🚀 Happy Coding!
