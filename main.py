import random
import cv2

class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.block_size = 20
        self.reset()
        self.auto_play = True  # Auto-play mode

    def toggle_auto_play(self):
        self.auto_play = not self.auto_play

    def reset(self):
        self.snake = [(100, 100)]
        self.direction = (self.block_size, 0)
        self.food = self.place_food()
        self.score = 0
        self.game_over = False

    def place_food(self):
        x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
        y = random.randint(0, (self.height - self.block_size) // self.block_size) * self.block_size
        return (x, y)

    def update(self, input_pos, frame):
        if self.game_over:
            cv2.putText(frame, "Game Over! Press 'R' to restart.", (100, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            return frame

        # Auto-play logic
        if self.auto_play:
            current_head = self.snake[0]
            dx = self.food[0] - current_head[0]
            dy = self.food[1] - current_head[1]

            step_x = self.block_size if dx > 0 else -self.block_size if dx < 0 else 0
            step_y = self.block_size if dy > 0 else -self.block_size if dy < 0 else 0

            head = (current_head[0] + step_x, current_head[1] + step_y)
        else:
            head = input_pos

        head = (head[0] // self.block_size * self.block_size, head[1] // self.block_size * self.block_size)
        self.snake.insert(0, head)

        # Eat food
        if abs(head[0] - self.food[0]) < self.block_size and abs(head[1] - self.food[1]) < self.block_size:
            self.score += 1
            self.food = self.place_food()
        else:
            self.snake.pop()

        # Collision with self
        if head in self.snake[1:]:
            self.game_over = True

        # Collision with wall
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            self.game_over = True

        # Draw snake
        for segment in self.snake:
            cv2.rectangle(frame, segment,
                          (segment[0] + self.block_size, segment[1] + self.block_size),
                          (0, 255, 0), -1)

        # Draw food
        cv2.circle(frame, (self.food[0] + self.block_size // 2, self.food[1] + self.block_size // 2),
                   self.block_size // 2, (0, 0, 255), -1)

        # Score
        mode = "AUTO" if self.auto_play else "HAND"
        cv2.putText(frame, f"Mode: {mode} | Score: {self.score}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return frame
