import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 800
BORDER_WIDTH = 60  # Non-playable border width
PLAYABLE_WIDTH = WIDTH - 2 * BORDER_WIDTH  # Width within playable area
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Endless Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock and fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)  # Reduced font size
big_font = pygame.font.SysFont("Arial", 50, bold=True)  # Large bold font for "Game Over"

# Car dimensions
CAR_WIDTH, CAR_HEIGHT = 50, 100

# Load assets
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT * 2))

player_car = pygame.image.load("car.png").convert_alpha()
player_car = pygame.transform.scale(player_car, (CAR_WIDTH, CAR_HEIGHT))

# Load obstacle cars
obstacle_cars = [
    pygame.image.load("obstacle_car1.png").convert_alpha(),
    pygame.image.load("obstacle_car2.png").convert_alpha(),
    pygame.image.load("obstacle_car3.png").convert_alpha(),
    pygame.image.load("obstacle_car4.png").convert_alpha(),
    pygame.image.load("obstacle_car5.png").convert_alpha(),
    pygame.image.load("obstacle_car6.png").convert_alpha(),
]

# Resize obstacle cars
obstacle_cars = [pygame.transform.scale(car, (CAR_WIDTH, CAR_HEIGHT)) for car in obstacle_cars]

# Game variables
player_x = BORDER_WIDTH + PLAYABLE_WIDTH // 2 - CAR_WIDTH // 2
player_y = HEIGHT - 150
player_speed = 7

obstacles = []
obstacle_speed = 5
spawn_timer = 0

score = 0
highest_score = 0

# Background scrolling variables
background_y = 0

# File to store the highest score
HIGHEST_SCORE_FILE = "highest_score.txt"

# Load highest score from file
def load_highest_score():
    global highest_score
    if os.path.exists(HIGHEST_SCORE_FILE):
        with open(HIGHEST_SCORE_FILE, "r") as file:
            try:
                highest_score = int(file.read())
            except ValueError:
                highest_score = 0

# Save highest score to file
def save_highest_score():
    with open(HIGHEST_SCORE_FILE, "w") as file:
        file.write(str(highest_score))

# Function to draw obstacles
def draw_obstacles():
    for obs in obstacles:
        screen.blit(obs["image"], obs["rect"].topleft)

# Function to display blurred game over screen
def display_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)  # 50% transparency
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    game_over_text = big_font.render("GAME OVER", True, RED)
    essay_text = font.render("Be careful", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(essay_text, (WIDTH // 2 - essay_text.get_width() // 2, HEIGHT // 2))

# Main game loop
def game_loop():
    global player_x, spawn_timer, score, obstacle_speed, background_y, highest_score

    load_highest_score()

    running = True
    while running:
        clock.tick(60)  # Cap the frame rate at 60 FPS

        # Scroll background at the same speed as obstacles
        background_y += obstacle_speed
        if background_y >= HEIGHT:
            background_y = 0

        # Draw background
        screen.blit(background, (0, background_y - HEIGHT))  # Upper part
        screen.blit(background, (0, background_y))  # Lower part

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Left arrow or 'A' key
            if player_x > BORDER_WIDTH:
                player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Right arrow or 'D' key
            if player_x < WIDTH - BORDER_WIDTH - CAR_WIDTH:
                player_x += player_speed

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > 50:  # Spawn every 50 frames
            obs_x = random.randint(BORDER_WIDTH, WIDTH - BORDER_WIDTH - CAR_WIDTH)
            obs_image = random.choice(obstacle_cars)
            obstacles.append({
                "rect": pygame.Rect(obs_x, -CAR_HEIGHT, CAR_WIDTH, CAR_HEIGHT),
                "image": obs_image
            })
            spawn_timer = 0
            score += 1

        # Move obstacles
        for obs in obstacles:
            obs["rect"].y += obstacle_speed

        # Remove off-screen obstacles
        obstacles[:] = [obs for obs in obstacles if obs["rect"].y < HEIGHT]

        # Check collisions
        player_rect = pygame.Rect(player_x, player_y, CAR_WIDTH, CAR_HEIGHT)
        for obs in obstacles:
            if player_rect.colliderect(obs["rect"]):
                print("Game Over!")
                if score > highest_score:
                    highest_score = score
                    save_highest_score()
                display_game_over()  # Show Game Over screen
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds
                running = False

        # Gradual speed increase
        if score % 10 == 0 and score > 0:
            obstacle_speed = 5 + score // 10  # Gradual increase in speed
            print(f"Speed increased to: {obstacle_speed}")

        # Draw player car and obstacles
        screen.blit(player_car, (player_x, player_y))
        draw_obstacles()

        # Display score and highest score
        score_text = font.render(f"Score: {score}", True, WHITE)
        highest_score_text = font.render(f"Highest Score: {highest_score}", True, WHITE)
        screen.blit(score_text, (10, 10))  # Current score at top-left
        screen.blit(highest_score_text, (WIDTH - 200, 10))  # Highest score at top-right

        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Run the game
game_loop()
