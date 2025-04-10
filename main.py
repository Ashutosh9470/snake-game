import cv2
import mediapipe as mp
from utils.snake import SnakeGame

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Snake Game instance
game = SnakeGame()

# Smoothening setup
smoothening = 0.2
prev_x, prev_y = 0, 0

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:  # Index fingertip
                    # Smooth coordinates
                    smoothed_x = int(prev_x + (cx - prev_x) * smoothening)
                    smoothed_y = int(prev_y + (cy - prev_y) * smoothening)
                    prev_x, prev_y = smoothed_x, smoothed_y

                    # Draw fingertip
                    cv2.circle(frame, (smoothed_x, smoothed_y), 15, (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, f'Index: {smoothed_x},{smoothed_y}', (smoothed_x+20, smoothed_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                    # Update snake game with smoothed finger position
                    frame = game.update((smoothed_x, smoothed_y), frame)

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    else:
        # If hand is not detected, still show Game Over message
        if game.game_over:
            frame = game.update((prev_x, prev_y), frame)

    cv2.imshow("Snake Game - Hand Controlled", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        game.reset()

cap.release()
cv2.destroyAllWindows()
