import pygame, copy, random


# CONSTANTS

# Window
WIDTH, HEIGHT = 700, 700
GRID = 35
SPEED = 10
# Colours
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# SETUP

# Window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
# Apple
apple_x = random.randint(0, (WIDTH / GRID) - 1)
apple_y = random.randint(0, (HEIGHT / GRID) - 1)

def randomize_apple(snake):
    global apple_x, apple_y
    
    apple_x = random.randint(0, (WIDTH / GRID) - 1)
    apple_y = random.randint(0, (HEIGHT / GRID) - 1)

    for part in snake:
        if part.x == apple_x and part.y == apple_y:
            randomize_apple(snake)

def draw_apple(win):
    pygame.draw.rect(win, RED, pygame.Rect(apple_x * GRID, apple_y * GRID, GRID, GRID))

# Snake class
class Snake:
    # Initiate
    def __init__(self, x, y):
        self.snake = [pygame.Vector2(x-2, y), pygame.Vector2(x-1, y), pygame.Vector2(x, y)]
        self.direction = 'RIGHT'
        self.x = x
        self.y = y

    # Move snake
    def move(self):
        self.snake.pop(0)

        if self.direction == 'RIGHT':
            # Move right
            self.x += 1
        elif self.direction == 'LEFT':
            # Move left
            self.x -= 1
        elif self.direction == 'UP':
            # Move up
            self.y -= 1
        else:
            # Move down
            self.y += 1
        self.snake.append(pygame.Vector2(self.x, self.y))

    # Draw snake
    def draw(self):
        for part in self.snake:
            pygame.draw.rect(win, GREEN, pygame.Rect(part.x * GRID, part.y * GRID, GRID, GRID))

    def die(self):
        if len(self.snake) > 1:
            snake_body = self.snake.copy()
            snake_body.pop()
            
            if self.snake[len(self.snake) - 1] in snake_body or self.snake[len(self.snake) - 1].x >= WIDTH / GRID or self.snake[len(self.snake) - 1].x <= -1 or self.snake[len(self.snake) - 1].y >= HEIGHT / GRID or self.snake[len(self.snake) - 1].y <= -1:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def grow(self):
        if self.snake[len(self.snake) - 1].x == apple_x and self.snake[len(self.snake) - 1].y == apple_y:
            self.snake.insert(0, copy.copy(self.snake[0]))
            randomize_apple(self.snake)


# Create snake
snake = Snake(3, 0)


# MAIN LOOP
def main():
    run = True
    while run:
        # Set the clock speed
        clock.tick(SPEED)

        # Clear the Screen
        win.fill(BLACK)


        for event in pygame.event.get():
            # If the close button is pressed, quit
            if event.type == pygame.QUIT:
                run = False
            
            # Change the snake's direction
            if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and not snake.direction == 'DOWN':
                        snake.direction = 'UP'
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and not snake.direction == 'UP':
                        snake.direction = 'DOWN'
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and not snake.direction == 'RIGHT':
                        snake.direction = 'LEFT'
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and not snake.direction == 'LEFT':
                        snake.direction = 'RIGHT'


        # Update the snake
        snake.move()
        snake.grow()
        snake.die()

        # Draw the snake
        snake.draw()

        # Draw the apple
        draw_apple(win)

        # Update the display
        pygame.display.update()


if __name__ == '__main__':
    main()
