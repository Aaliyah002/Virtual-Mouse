import cv2
import mediapipe as mp
import pyautogui 
import time
import math

pyautogui.FAILSAFE = False

# ================= INIT =================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# gesture control
click_times = []
click_cooldown = 0.5
scroll_mode = False
freeze_cursor = False

# NEW FEATURES
screenshot_cooldown = 2
last_screenshot_time = 0

# EYE SCROLL
last_eye_scroll = 0
eye_scroll_cooldown = 0.5

# ZOOM
zoom_mode = False
prev_dist = 0

screen_w, screen_h = pyautogui.size()
print("\nHand + Eye Mouse Control Started")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame")
        break
    
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process both hand & face
    result = hands.process(rgb)
    face_results = face_mesh.process(rgb)

    current_time = time.time()
    fingers = [0,0,0,0]  # default (IMPORTANT FIX)


    # ================= HAND TRACKING =================
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # landmarks
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]

            fingers = [
                1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y else 0
                for tip in [8, 12, 16, 20]
            ]

            # ================= CLICK =================
            dist = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)

            if dist < 0.06:
                if not freeze_cursor:
                    freeze_cursor = True
                    click_times.append(current_time)

                    if len(click_times) >= 2 and click_times[-1] - click_times[-2] < 0.4:
                        pyautogui.doubleClick()
                        cv2.putText(frame, "Double Click", (100,100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                        click_times = []
                    else:
                        pyautogui.click()
                        cv2.putText(frame, "Single Click", (100,100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            else:
                if freeze_cursor:
                    time.sleep(0.1)
                freeze_cursor = False        

            # ================= MOVE =================
            if not freeze_cursor:
                screen_x = int(index_tip.x * screen_w)
                screen_y = int(index_tip.y * screen_h)
                pyautogui.moveTo(screen_x, screen_y, duration=0.05)

            # ================= SCREENSHOT =================
            if fingers == [1,1,0,0]:
                if current_time - last_screenshot_time > screenshot_cooldown:
                    filename = f"screenshot_{int(current_time)}.png"
                    pyautogui.screenshot(filename)
                    last_screenshot_time = current_time
                    cv2.putText(frame, "Screenshot", (100,150),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

            # ================= SCROLL (HAND) =================
            if sum(fingers) == 4:
                scroll_mode = True
            else:
                scroll_mode = False
                
            if scroll_mode:
                if index_tip.y < 0.4:
                    pyautogui.scroll(60)
                    cv2.putText(frame, "Scroll Up", (100,100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                elif index_tip.y > 0.6:
                    pyautogui.scroll(-60)
                    cv2.putText(frame, "Scroll Down", (100,100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # ================= ZOOM =================
            zoom_dist = dist

            if dist > 0.06 and fingers == [1,0,0,0]:
                zoom_mode = True

                if prev_dist != 0:
                    if zoom_dist - prev_dist > 0.02:
                        pyautogui.hotkey('ctrl', '+')
                        cv2.putText(frame, "Zoom In", (100,200),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                    elif prev_dist - zoom_dist > 0.02:
                        pyautogui.hotkey('ctrl', '-')
                        cv2.putText(frame, "Zoom Out", (100,200),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                prev_dist = zoom_dist
            else:
                zoom_mode = False
                prev_dist = 0

    # ================= EYE =================
    if face_results.multi_face_landmarks:
        face_landmarks = face_results.multi_face_landmarks[0]

        iris = face_landmarks.landmark[474]

        h, w, _ = frame.shape
        eye_x = int(iris.x * w)
        eye_y = int(iris.y * h)

        # draw tracking
        cv2.circle(frame, (eye_x, eye_y), 5, (0,255,255), -1)

        cv2.putText(frame, f"EyeY: {iris.y:.2f}", (30,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        # ================= CONTROLLED EYE SCROLL =================
        if fingers == [1,1,1,1]:  # ONLY when hand open

            if current_time - last_eye_scroll > eye_scroll_cooldown:
                if iris.y > 0.6:
                    pyautogui.scroll(-50)
                    last_eye_scroll = current_time

                elif iris.y < 0.4:
                    pyautogui.scroll(50)
                    last_eye_scroll = current_time

    cv2.imshow("Live Video", frame)

    if cv2.waitKey(1) == ord('a'):
        break

cap.release()
cv2.destroyAllWindows()
