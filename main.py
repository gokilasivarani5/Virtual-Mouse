import cv2
import mediapipe as mp
import pyautogui
import random
import util
from pynput.mouse import Button, Controller
import tkinter as tk
from tkinter import messagebox
import time

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

draw = mp.solutions.drawing_utils
prev_scroll_pos = None
dragging = False
message = ""
message_time = 0

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)
        pyautogui.moveTo(x, y)

def is_left_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmark_list, thumb_index_dist):
    middle_finger_bent = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
        middle_finger_bent and
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
    index_tip_y = landmarks[8][1]
    index_pip_y = landmarks[6][1]
    middle_tip_y = landmarks[12][1]
    middle_pip_y = landmarks[10][1]
    ring_tip_y = landmarks[16][1]
    ring_pip_y = landmarks[14][1]
    pinky_tip_y = landmarks[20][1]
    pinky_pip_y = landmarks[18][1]

    return (
        index_tip_y > index_pip_y and
        middle_tip_y < middle_pip_y and
        ring_tip_y < ring_pip_y and
        pinky_tip_y < pinky_pip_y
    )

def get_finger_states(landmark_list):
    if len(landmark_list) < 21:
        return [False] * 5
    finger_states = []
    finger_states.append(landmark_list[4][0] > landmark_list[3][0])
    finger_ids = [(8, 6), (12, 10), (16, 14), (20, 18)]
    for tip, pip in finger_ids:
        finger_states.append(landmark_list[tip][1] < landmark_list[pip][1])
    return finger_states  # [Thumb, Index, Middle, Ring, Pinky]

def is_drag_pose(landmark_list):
    fingers = get_finger_states(landmark_list)
    return fingers[2] and not fingers[0] and not fingers[1] and not fingers[3] and not fingers[4]

def handle_scroll(landmarks, frame):
    global prev_scroll_pos, message, message_time
    if is_scroll_pose(landmarks):
        x = int(landmarks[8][0] * screen_width)
        y = int(landmarks[8][1] * screen_height)
        current_y = landmarks[8][1]
        current_x = landmarks[8][0]
        if prev_scroll_pos is not None:
            dy = current_y - prev_scroll_pos[1]
            dx = current_x - prev_scroll_pos[0]
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

def detect_gesture(frame, landmark_list, processed):
    global dragging, message, message_time
    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])
        if is_scroll_pose(landmark_list):
            handle_scroll(landmark_list, frame)
            return
        if is_drag_pose(landmark_list):
            if not dragging:
                mouse.press(Button.left)
                dragging = True
                message = "Drag Start"
                message_time = time.time()
            move_mouse(index_finger_tip)
        else:
            if dragging:
                mouse.release(Button.left)
                dragging = False
                message = "Drag End"
                message_time = time.time()
            if thumb_index_dist < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
                move_mouse(index_finger_tip)
            elif is_left_click(landmark_list, thumb_index_dist):
                mouse.press(Button.left)
                mouse.release(Button.left)
                message = "Left Click"
                message_time = time.time()
            elif is_right_click(landmark_list, thumb_index_dist):
                mouse.press(Button.right)
                mouse.release(Button.right)
                message = "Right Click"
                message_time = time.time()
            elif is_double_click(landmark_list, thumb_index_dist):
                pyautogui.doubleClick()
                message = "Double Click"
                message_time = time.time()
            elif is_screenshot(landmark_list, thumb_index_dist):
                im1 = pyautogui.screenshot()
                label = random.randint(1, 1000)
                filename = f'my_screenshot_{label}.png'
                im1.save(filename)
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Screenshot Taken", f"Screenshot saved as '{filename}'")
                root.destroy()
                message = "Screenshot Saved"
                message_time = time.time()

def show_message(frame):
    if message and time.time() - message_time < 5:
        cv2.putText(frame, message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 255), 3)

def main():
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)
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
