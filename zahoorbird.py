import pygame
import sys
import random
import json
from datetime import datetime

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_SPEED = 3
PIPE_GAP = 150
GRAVITY = 0.5
JUMP_STRENGTH = -8
FPS = 60
# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MzahRAH Bird - Eid Edition")
clock = pygame.time.Clock()

# Load Assets
def load_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except pygame.error:
        return pygame.Surface(size)

bg_img = load_image("Python_projects/eidbg.png", (WIDTH, HEIGHT))
bird_img = load_image("Python_projects/bird.png", (40, 40))
pipe_img = load_image("Python_projects/frozen_pipe.png", (60, 150))

# Sound System
pygame.mixer.init()
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None

SOUNDS = {
    "flap": load_sound("Python_projects/flap.wav"),
    "score": load_sound("Python_projects/score.wav"),
    "hit": load_sound("Python_projects/hit.wav")
}

# Game State
class GameState:
    def __init__(self):
        self.reset()
        self.high_score = 0
        self.load_high_score()
    
    def reset(self):
        self.bird_y = HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = [self.create_pipe()]
        self.score = 0
        self.game_active = False
        self.in_menu = True
        self.selected_menu_index = 0

    def create_pipe(self):
        return {"x": WIDTH, "y": random.randint(100, HEIGHT - 200), "passed": False}

    def load_high_score(self):
        try:
            with open("highscore.json", "r") as f:
                self.high_score = json.load(f).get("high_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_score = 0

    def save_high_score(self):
        with open("highscore.json", "w") as f:
            json.dump({"high_score": self.high_score, "date": str(datetime.now())}, f)

game_state = GameState()

# Draw Text
def draw_text(text, size, pos, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Main Menu
def main_menu():
    menu_items = ["Play", "Resume", "Exit"]
    while game_state.in_menu:
        screen.blit(bg_img, (0, 0))
        draw_text("Zahoor Bird", 50, (WIDTH//2 - 100, 50))
        draw_text("Eid Edition", 40, (WIDTH//2 - 80, 120))

        for index, item in enumerate(menu_items):
            color = (100, 200, 100) if index == game_state.selected_menu_index else (50, 150, 50)
            pygame.draw.rect(screen, color, (WIDTH//2 - 100, 200 + index * 60, 200, 50), border_radius=10)
            draw_text(item, 30, (WIDTH//2 - 40, 210 + index * 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    game_state.selected_menu_index = (game_state.selected_menu_index + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    game_state.selected_menu_index = (game_state.selected_menu_index - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    action = menu_items[game_state.selected_menu_index]
                    if action == "Play":
                        game_state.reset()
                        game_state.game_active = True
                        game_loop()
                    elif action == "Resume" and game_state.game_active:
                        game_loop()
                    elif action == "Exit":
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(FPS)

# Game Loop
def game_loop():
    while game_state.game_active:
        handle_input()
        update_game()
        draw_game()
        pygame.display.update()
        clock.tick(FPS)

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_state.bird_velocity = JUMP_STRENGTH
                if SOUNDS["flap"]:
                    SOUNDS["flap"].play()
            if event.key == pygame.K_ESCAPE:
                game_state.in_menu = True
                main_menu()

def update_game():
    game_state.bird_velocity += GRAVITY
    game_state.bird_y += game_state.bird_velocity

    for pipe in game_state.pipes:
        pipe["x"] -= PIPE_SPEED
        if pipe["x"] + 60 < 50 and not pipe["passed"]:
            game_state.score += 1
            pipe["passed"] = True
            if SOUNDS["score"]:
                SOUNDS["score"].play()

    if game_state.pipes[-1]["x"] < WIDTH - 300:
        game_state.pipes.append(game_state.create_pipe())

    bird_rect = pygame.Rect(50, int(game_state.bird_y), 40, 40)
    if bird_rect.top < 0 or bird_rect.bottom > HEIGHT:
        game_over()

    for pipe in game_state.pipes:
        rect_top = pygame.Rect(int(pipe["x"]), int(pipe["y"] - 150), 60, 150)
        rect_bottom = pygame.Rect(int(pipe["x"]), int(pipe["y"] + PIPE_GAP), 60, 150)
        if bird_rect.colliderect(rect_top) or bird_rect.colliderect(rect_bottom):
            game_over()

def draw_game():
    screen.blit(bg_img, (0, 0))
    screen.blit(bird_img, (50, int(game_state.bird_y)))
    for pipe in game_state.pipes:
        screen.blit(pipe_img, (int(pipe["x"]), int(pipe["y"] - 150)))
        screen.blit(pipe_img, (int(pipe["x"]), int(pipe["y"] + PIPE_GAP)))
    draw_text(f"Score: {game_state.score}", 30, (10, 10))

def game_over():
    game_state.game_active = False
    draw_text("Game Over", 50, (WIDTH//2 - 100, HEIGHT//2 - 50))
    pygame.display.update()
    pygame.time.delay(2000)
    main_menu()

# Start Game
main_menu()
