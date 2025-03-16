import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
from tracker import *
import serial
import time

# Initialize serial communication
ser = serial.Serial('COM3', 115200)  # Replace 'COM3' with your serial port
time.sleep(2)  # Wait for the serial connection to initialize

# Load YOLO model
model = YOLO('best.pt')

# Load class names
with open("coco1.txt", "r") as my_file:
    class_list = my_file.read().splitlines()

# Line position for counting
cy1 = 427
offset = 6

# Initialize trackers and counters
tracker_bus = Tracker()
tracker_car = Tracker()
tracker_auto = Tracker()
tracker_motorcycle = Tracker()

bus = []
car = []
auto_rikshaw = []
motorcycle = []

# Open video
cap = cv2.VideoCapture('id4.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame
    frame = cv2.resize(frame, (1020, 500))

    # Run YOLO prediction
    results = model.predict(frame)
    detections = results[0].boxes.data

    # Process detection results
    list_bus = []
    list_car = []
    list_auto = []
    list_motorcycle = []

    for row in detections:
        x1, y1, x2, y2, conf, cls = map(int, row[:6])
        class_name = class_list[cls]

        if 'bus' in class_name:
            list_bus.append([x1, y1, x2, y2])
        elif 'car' in class_name:
            list_car.append([x1, y1, x2, y2])
        elif 'auto-rikshaw' in class_name:
            list_auto.append([x1, y1, x2, y2])
        elif 'motor-cycle' in class_name:
            list_motorcycle.append([x1, y1, x2, y2])

    # Update trackers
    tracked_buses = tracker_bus.update(list_bus)
    tracked_cars = tracker_car.update(list_car)
    tracked_autos = tracker_auto.update(list_auto)
    tracked_motorcycles = tracker_motorcycle.update(list_motorcycle)

    # Count objects crossing the line
    for bbox in tracked_buses:
        x3, y3, x4, y4, id = bbox
        cy = (y3 + y4) // 2
        if cy1 - offset < cy < cy1 + offset and id not in bus:
            bus.append(id)

    for bbox in tracked_cars:
        x3, y3, x4, y4, id = bbox
        cy = (y3 + y4) // 2
        if cy1 - offset < cy < cy1 + offset and id not in car:
            car.append(id)

    for bbox in tracked_autos:
        x3, y3, x4, y4, id = bbox
        cy = (y3 + y4) // 2
        if cy1 - offset < cy < cy1 + offset and id not in auto_rikshaw:
            auto_rikshaw.append(id)

    for bbox in tracked_motorcycles:
        x3, y3, x4, y4, id = bbox
        cy = (y3 + y4) // 2
        if cy1 - offset < cy < cy1 + offset and id not in motorcycle:
            motorcycle.append(id)

    # Count the totals
    count_bus = len(bus)
    count_car = len(car)
    count_auto = len(auto_rikshaw)
    count_motorcycle = len(motorcycle)

    # Display on frame
    cvzone.putTextRect(frame, f'Bus Count: {count_bus}', (50, 50), scale=2, thickness=2)
    cvzone.putTextRect(frame, f'Car Count: {count_car}', (50, 100), scale=2, thickness=2)
    cvzone.putTextRect(frame, f'Auto Count: {count_auto}', (50, 150), scale=2, thickness=2)
    cvzone.putTextRect(frame, f'Motorcycle Count: {count_motorcycle}', (50, 200), scale=2, thickness=2)
    cv2.line(frame, (0, cy1), (frame.shape[1], cy1), (255, 255, 255), 2)

    # Show the frame
    cv2.imshow("Frame", frame)

    # Send counts via Serial
    data_to_send = f"{count_bus},{count_car},{count_auto},{count_motorcycle}\n"
    ser.write(data_to_send.encode('utf-8'))

    if cv2.waitKey(0) & 0xFF == 27:  # Press Esc to exit
        break
    # if cv2.waitKey(1)&0xFF==27:
    #     break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()
