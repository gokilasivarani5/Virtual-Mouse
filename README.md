# Virtual Mouse using Hand Gestures

This is a **Virtual Mouse** system built with Python, OpenCV, and MediaPipe that allows users to **control the mouse cursor** using **hand gestures** detected via webcam. Additional gestures can be used for **left click, right click, double click, drag, scroll**, and even **screenshot**.
---
## Features

-  Real-time hand tracking using **MediaPipe**
-  Mouse movement with **index finger**
-  Left Click, Right Click, and Double Click gestures
- Take Screenshot using specific hand gesture
-  Drag and Drop gesture
-  Vertical and Horizontal scrolling gesture
-  On-screen message display using OpenCV
-  press 'q' to quit

---

##  Tech Stack

- **Python 3.10**
- [MediaPipe](https://google.github.io/mediapipe/)
- [OpenCV](https://opencv.org/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)
- [Pynput](https://pynput.readthedocs.io/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- **Numpy**

---

##  How It Works

1. Capture live video from webcam.
2. Use **MediaPipe** to detect hand landmarks.
3. Map **index finger tip position** to mouse position.
4. Detect gestures based on **finger angles and distances**.
5. Trigger mouse or keyboard events via **PyAutoGUI** or **pynput**.

---


##  Requirements

Install required packages using:

pip install opencv-python mediapipe pyautogui pynput numpy
---


## Mouse Move
<img width="579" height="326" alt="image" src="https://github.com/user-attachments/assets/3586f1d1-44e8-468c-a044-d2c99c90225f" />
## Right Click
<img width="596" height="337" alt="image" src="https://github.com/user-attachments/assets/064c1998-060e-44c0-8bf2-d7fb9c8e1dd0" />
## Left Click
<img width="596" height="337" alt="image" src="https://github.com/user-attachments/assets/02406a0c-e4b5-4a67-bb35-cb4b6b7a751b" />
## Double Click
<img width="596" height="336" alt="image" src="https://github.com/user-attachments/assets/53454daf-0d1e-4765-924c-ce6e1d966f0c" />
## Drag Start
<img width="596" height="337" alt="image" src="https://github.com/user-attachments/assets/32fc6116-f747-494a-ab7b-1872a1435a46" />
## Drag End
<img width="596" height="337" alt="image" src="https://github.com/user-attachments/assets/cb8f72e1-5c6f-4fc6-863a-65b345778e5f" />
## Scrolling
<img width="596" height="337" alt="image" src="https://github.com/user-attachments/assets/d90bbe41-c2ee-4121-8ee0-96050b4c74bc" />
## Screenshot
<img width="596" height="337" alt="image" src="https://github.com/user-attachments/assets/63e96082-ca24-4766-b172-cbc9f616be1f" />
