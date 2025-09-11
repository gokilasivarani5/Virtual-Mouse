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


# Virtual-Mouse

