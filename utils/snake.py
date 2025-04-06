import cv2
import numpy as np
import math
import random

class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.points = []
        self.lengths = []
        self.current_length = 0
        self.allowed_length = 150
        self.previous_head = (0, 0)
        self.food = self._generate_food()
        self.score = 0
        self.game_over = False

    def _generate_food(self):
        return random.randint(100, 500), random.randint(100, 400)

    def update(self, current_head, img):
        if self.game_over:
            cv2.putText(img, "GAME OVER", (180, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            cv2.putText(img, "Press 'R' to Restart", (150, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            return img

        if self.previous_head == (0, 0):
            self.previous_head = current_head

        self.points.append(current_head)
        distance = math.hypot(current_head[0] - self.previous_head[0],
                              current_head[1] - self.previous_head[1])
        self.lengths.append(distance)
        self.current_length += distance
        self.previous_head = current_head

        while self.current_length > self.allowed_length:
            self.points.pop(0)
            removed_length = self.lengths.pop(0)
            self.current_length -= removed_length

        # Draw snake
        for i in range(1, len(self.points)):
            cv2.line(img, self.points[i - 1], self.points[i], (0, 255, 0), 15)

        # Draw food
        fx, fy = self.food
        cv2.circle(img, (fx, fy), 10, (0, 0, 255), cv2.FILLED)

        # Check for food collision
        if math.hypot(current_head[0] - fx, current_head[1] - fy) < 20:
            self.food = self._generate_food()
            self.allowed_length += 30
            self.score += 1

        # Check for self-collision (skip last 15 points to avoid false hit)
        for point in self.points[:-15]:
            if math.hypot(current_head[0] - point[0], current_head[1] - point[1]) < 15:
                self.game_over = True
                break

        # Show score
        cv2.putText(img, f'Score: {self.score}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return img
