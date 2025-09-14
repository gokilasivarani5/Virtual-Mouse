"""
Virtual Mouse using Hand Gestures
---------------------------------
This script uses OpenCV, MediaPipe, PyAutoGUI, and Pynput to let you
control the computer mouse through real-time hand gestures captured by a webcam.

Features:
    • Move mouse cursor
    • Left click, right click, double click
    • Drag & drop
    • Vertical & horizontal scrolling
    • Take a screenshot with confirmation popup
Press 'q' to quit.
"""

import cv2
import mediapipe as mp
import pyautogui
import random
import util                 # Custom helper functions (distance, angle, etc.)
from pynput.mouse import Button, Controller
import tkinter as tk
from tkinter import messagebox
import time

# Mouse controller and screen size
mouse = Controller()
screen_width, screen_height = pyautogui.size()

# Initialize MediaPipe Hands with recommended parameters
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,     # Real-time stream
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

draw = mp.solutions.drawing_utils   # For drawing hand landmarks

# State variables
prev_scroll_pos = None
dragging = False
message = ""        # Message to overlay on frame (e.g., "Left Click")
message_time = 0    # Timestamp to auto-clear messages

# ---------- Utility Functions ----------

def find_finger_tip(processed):
    """Return the index finger tip landmark if a hand is detected."""
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None

def move_mouse(index_finger_tip):
    """Move mouse pointer according to index finger position."""
    if index_finger_tip:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)  # divide Y to reduce sensitivity
        pyautogui.moveTo(x, y)

# --- Gesture checks: use landmark angles & distances to classify actions ---

def is_left_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmark_list, thumb_index_dist):
    middle_bent = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
        middle_bent and
        thumb_index_dist > 50
    )

def is_double_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        thumb_index_dist > 50
    )

def is_screenshot(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        thumb_index_dist < 50
    )

def is_scroll_pose(landmarks):
    """Detect pose for scrolling: index finger down, others up."""
    index_tip_y, index_pip_y = landmarks[8][1], landmarks[6][1]
    middle_tip_y, middle_pip_y = landmarks[12][1], landmarks[10][1]
    ring_tip_y, ring_pip_y = landmarks[16][1], landmarks[14][1]
    pinky_tip_y, pinky_pip_y = landmarks[20][1], landmarks[18][1]
    return (
        index_tip_y > index_pip_y and
        middle_tip_y < middle_pip_y and
        ring_tip_y   < ring_pip_y and
        pinky_tip_y  < pinky_pip_y
    )

def get_finger_states(landmark_list):
    """Return a list [Thumb, Index, Middle, Ring, Pinky] with True if finger is up."""
    if len(landmark_list) < 21:
        return [False] * 5
    states = []
    states.append(landmark_list[4][0] > landmark_list[3][0])  # Thumb check
    for tip, pip in [(8,6),(12,10),(16,14),(20,18)]:
        states.append(landmark_list[tip][1] < landmark_list[pip][1])
    return states

def is_drag_pose(landmark_list):
    """Drag when only middle finger is up."""
    fingers = get_finger_states(landmark_list)
    return fingers[2] and not any(fingers[i] for i in [0,1,3,4])

def handle_scroll(landmarks, frame):
    """Scroll vertically or horizontally based on index finger movement."""
    global prev_scroll_pos, message, message_time
    if is_scroll_pose(landmarks):
        current_x, current_y = landmarks[8]
        if prev_scroll_pos:
            dx = current_x - prev_scroll_pos[0]
            dy = current_y - prev_scroll_pos[1]
            if abs(dy) > abs(dx):
                pyautogui.scroll(-int(dy * 200))
                message = "Scrolling Vertically"
            else:
                pyautogui.hscroll(int(dx * 200))
                message = "Scrolling Horizontally"
            message_time = time.time()
        prev_scroll_pos = (current_x, current_y)
    else:
        prev_scroll_pos = None

# ---------- Main Gesture Detection ----------

def detect_gesture(frame, landmark_list, processed):
    """
    Identify gesture type and perform the corresponding mouse action.
    Updates 'message' for on-screen feedback.
    """
    global dragging, message, message_time

    if len(landmark_list) < 21:
        return

    index_finger_tip = find_finger_tip(processed)
    thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

    # Scroll gesture
    if is_scroll_pose(landmark_list):
        handle_scroll(landmark_list, frame)
        return

    # Drag & move gesture
    if is_drag_pose(landmark_list):
        if not dragging:
            mouse.press(Button.left)
            dragging = True
            message, message_time = "Drag Start", time.time()
        move_mouse(index_finger_tip)
    else:
        if dragging:
            mouse.release(Button.left)
            dragging = False
            message, message_time = "Drag End", time.time()

        # Pointer move without click
        if thumb_index_dist < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
        elif is_left_click(landmark_list, thumb_index_dist):
            mouse.click(Button.left)
            message, message_time = "Left Click", time.time()
        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.click(Button.right)
            message, message_time = "Right Click", time.time()
        elif is_double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            message, message_time = "Double Click", time.time()
        elif is_screenshot(landmark_list, thumb_index_dist):
            # Capture and save screenshot with a random label
            filename = f"my_screenshot_{random.randint(1, 1000)}.png"
            pyautogui.screenshot().save(filename)
            # Pop-up confirmation
            root = tk.Tk(); root.withdraw()
            messagebox.showinfo("Screenshot Taken", f"Saved as {filename}")
            root.destroy()
            message, message_time = "Screenshot Saved", time.time()

def show_message(frame):
    """Display action message for 5 seconds on the OpenCV window."""
    if message and time.time() - message_time < 5:
        cv2.putText(frame, message, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 255), 3)

# ---------- Entry Point ----------

def main():
    """Capture webcam frames, process hand landmarks, and respond to gestures."""
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            # Collect normalized landmark coordinates
            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)
            show_message(frame)

            cv2.imshow('Virtual Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
