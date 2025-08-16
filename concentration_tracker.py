import cv2
import mediapipe as mp
import math
import threading
import tkinter as tk

# MediaPipe and OpenCV setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
running = False  # Flag to control tracking loop


# EAR calculation
def eye_aspect_ratio(landmarks, eye_indices):
    left = landmarks[eye_indices[0]]
    right = landmarks[eye_indices[3]]
    top = landmarks[eye_indices[1]]
    bottom = landmarks[eye_indices[2]]

    hor_dist = math.dist([left.x, left.y], [right.x, right.y])
    ver_dist = math.dist([top.x, top.y], [bottom.x, bottom.y])
    return ver_dist / hor_dist if hor_dist != 0 else 0


# Gaze ratio
def get_gaze_ratio(landmarks, eye_indices, iris_index):
    left = landmarks[eye_indices[0]]
    right = landmarks[eye_indices[3]]
    iris = landmarks[iris_index]

    eye_width = right.x - left.x
    iris_pos = iris.x - left.x
    return iris_pos / eye_width if eye_width != 0 else 0.5


# Focus mode loop
def focus_mode():
    global running, cap

    while running and cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        status = "Distracted"
        color = (0, 0, 255)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark

                left_eye = [33, 160, 158, 133]
                right_eye = [362, 385, 387, 263]
                left_iris_index = 468
                right_iris_index = 473

                left_ear = eye_aspect_ratio(landmarks, left_eye)
                right_ear = eye_aspect_ratio(landmarks, right_eye)
                avg_ear = (left_ear + right_ear) / 2

                left_gaze = get_gaze_ratio(landmarks, left_eye, left_iris_index)
                right_gaze = get_gaze_ratio(landmarks, right_eye, right_iris_index)
                avg_gaze = (left_gaze + right_gaze) / 2

                if avg_ear > 0.21 and 0.35 < avg_gaze < 0.65:
                    status = "Focused"
                    color = (0, 255, 0)

                mp_drawing.draw_landmarks(
                    frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                    mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1)
                )

        cv2.putText(frame, f'Status: {status}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, color, 3)

        cv2.imshow("Concentration Tracker", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()


# Start tracking
def start_focus():
    global running
    if not running:
        running = True
        thread = threading.Thread(target=focus_mode)
        thread.start()


# Stop tracking
def stop_focus():
    global running
    running = False


# GUI setup
root = tk.Tk()
root.title("Focus Mode Tracker")
root.geometry("400x200")
root.resizable(False, False)

title = tk.Label(root, text="Concentration Tracker", font=("Times New Roman", 20, "bold"))
title.pack(pady=20)

start_button = tk.Button(root, text="Start Focus Mode ON", command=start_focus, font=("Times New Roman", 14), bg="green", fg="White")
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_focus, font=("Times New Roman", 14), bg="red", fg="white")
stop_button.pack(pady= 3)

root.protocol("WM_DELETE_WINDOW", lambda: [stop_focus(), root.destroy()])
root.mainloop()
