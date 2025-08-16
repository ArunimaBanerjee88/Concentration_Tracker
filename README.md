# Focus Mode Tracker

A real-time **Concentration Tracker** built using **OpenCV**, **MediaPipe**, and **Tkinter**.  
It uses your **webcam** to detect **eye movements** and **gaze direction**, determining whether you are **Focused** or **Distracted**.

---

## Features

-  Real-time **eye & gaze tracking**
-  Displays **status**: *Focused* or *Distracted*
- Runs face tracking in a **separate thread** (smooth & responsive UI)
-  Simple and clean **Tkinter GUI**
  -  Start Focus Mode button  
  -  Stop button  

---

##  How It Works

The tracker uses **MediaPipe FaceMesh** to detect **eye landmarks** and **iris position**.

-  Calculates **Eye Aspect Ratio (EAR)** → checks if eyes are open  
-  Tracks **iris position** inside the eye → estimates gaze direction  
-  Combines both signals → determines your **focus level**  

---

##  Installation

1. **Clone this repository** or download the source code:
   ```bash
    git clone https://github.com/your-username/concentration_tracker.git
   cd concentration_tracker
Make sure you have Python 3.8+ installed.

2. Install the required libraries:

pip install opencv-python mediapipe

## Future Improvements

Add a distraction timer to measure focus duration

Generate session reports (focus % over time)



