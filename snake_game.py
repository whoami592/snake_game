import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game by Mr. Sabaz Ali Khan")
clock = pygame.time.Clock()

# Font for score and banner
font = pygame.font.SysFont("monospace", 30)

# Stylish ASCII Banner
BANNER = """
  _____ _          _ _       
 | __  | |__   ___| | | ___  
 |    -| '_ \ / __| | |/ _ \ 
 |__|\_|_.__/ \___|_|_|\___/
        SNAKE GAME
    Coded by Pakistani Ethical Hacker
       Mr. Sabaz Ali Khan
"""

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
    
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()
    
    def grow(self):
        self.length += 1
    
    def collides_with_self(self):
        return self.body[0] in self.body[1:]

class Food:
    def __init__(self):
        self.position = self.random_position()
    
    def random_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def respawn(self, snake_body):
        while True:
            pos = self.random_position()
            if pos not in snake_body:
                self.position = pos
                break

def setup():
    global snake, food, score, game_over
    snake = Snake()
    food = Food()
    score = 0
    game_over = False
    print(BANNER)  # Display banner in console

def draw():
    screen.fill(BLACK)
    
    # Draw snake
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Draw food
    pygame.draw.rect(screen, RED, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw game over screen
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, CYAN)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
    
    pygame.display.flip()

def update_loop():
    global score, game_over
    if game_over:
        return
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, 1):
                snake.direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                snake.direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                snake.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                snake.direction = (1, 0)
            elif event.key == pygame.K_r and game_over:
                setup()
    
    # Move snake
    snake.move()
    
    # Check collisions
    if snake.body[0] == food.position:
        snake.grow()
        score += 1
        food.respawn(snake.body)
    
    if snake.collides_with_self():
        game_over = True
    
    draw()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())