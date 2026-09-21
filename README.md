# Virtual Mouse

## About

This is a computer vision-based virtual mouse that allows users to control their computer using **hand gestures and eye movements**.

The project uses a webcam to detect hand and facial landmarks in real time. These landmarks are processed using **OpenCV** and **MediaPipe**, while **PyAutoGUI** converts recognized gestures into computer actions such as cursor movement, clicking, scrolling, zooming, and screenshots.

The goal of this project is to provide a simple **touchless human-computer interaction system** without requiring a physical mouse.

---

## Tech Stack

- **Python** — Core programming language
- **OpenCV** — Real-time video capture and image processing
- **MediaPipe** — Hand and facial landmark detection
- **PyAutoGUI** — Mouse, keyboard, and screenshot automation
- **NumPy** — Numerical operations and data processing

---

## Features

- **Cursor Control** — Move the mouse cursor using your index finger.
- **Single Click** — Perform a left click using a thumb-index finger pinch.
- **Double Click** — Perform a double click using two consecutive pinch gestures.
- **Scrolling** — Scroll up and down using hand gestures.
- **Eye-Controlled Scrolling** — Control scrolling using vertical eye movement.
- **Screenshot Capture** — Capture a screenshot using an index and middle finger gesture.
- **Zoom In / Out** — Zoom using changes in the thumb-index finger distance.
- **Real-Time Tracking** — Detect hand and facial landmarks through the webcam in real time.
- **Touchless Interaction** — Perform common computer operations without physically touching a mouse.

---

## Gesture Control

| Gesture | Action |
|---|---|
| **Move Index Finger** | Moves the mouse cursor across the screen |
| **Thumb + Index Finger Pinch** | Performs a single left click |
| **Two Quick Pinches** | Performs a double click |
| **Index + Middle Fingers Extended** | Captures a screenshot |
| **Whole Palm + All Fingers Up** | Scrolls upward |
| **Whole Palm + All Fingers Down** | Scrolls downward |
| **Open Hand + Eye Movement** | Controls scrolling using vertical eye movement |
| **Thumb Extended + Change in Thumb-Index Distance** | Performs Zoom In / Zoom Out |
| **Press `A`** | Exits the application |
