import pygame
import time
import sys

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mission 109")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 32)

# Create placeholder male character (red rectangle)
male_character = pygame.Surface((120, 180))
male_character.fill(RED)

# Load female images with error handling
female_images = {
    "normal": pygame.Surface((120, 180)),
    "strict": pygame.Surface((120, 180)),
    "happy": pygame.Surface((120, 180))
}
for img in female_images.values():
    img.fill(BLUE)  # Blue placeholder

current_female_image = female_images["normal"]

# Load sounds with error handling
try:
    click_sound = pygame.mixer.Sound("click.wav")
    success_sound = pygame.mixer.Sound("success.wav")
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Sound error:", e)

# Game scenes
scenes = [
    {"text": "You proposed to her...\nbut she rejected you.", "choices": ["Feel sad", "Move on"]},
    {"text": "'Work or study only,' she said.\nHer boundaries are clear.", "choices": ["Respect", "Push boundaries"]},
    {"text": "Time to prove yourself!\nMini Challenge: What is 2 + 2?", "choices": []},
    {"text": "You immerse yourself in Data Science.\nYour skills and hard work pay off.", "choices": ["Work hard", "Procrastinate"]},
    {"text": "Years later, you're very successful.\nWhat do you do now?", "choices": ["Talk to her", "Move forward"]}
]

# Game state
state = {
    "boundaries": None,
    "effort": None,
    "mini_success": False
}

scene_index = 0
progress = 0

def draw_text(text, x, y):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        render = font.render(line, True, BLACK)
        screen.blit(render, (x, y + i * 30))

def draw_scene():
    screen.fill(WHITE)
    # Draw characters
    screen.blit(male_character, (50, HEIGHT - 250))
    screen.blit(current_female_image, (WIDTH - 200, HEIGHT - 250))
    
    # Dialogue box
    pygame.draw.rect(screen, BLUE, (50, 50, WIDTH - 100, 100))
    draw_text(scenes[scene_index]["text"], 70, 70)

    # Choices
    for i, choice in enumerate(scenes[scene_index]["choices"]):
        pygame.draw.rect(screen, GRAY, (50, 200 + i * 60, 300, 50))
        draw_text(choice, 70, 215 + i * 60)

    # Progress bar
    pygame.draw.rect(screen, BLACK, (50, HEIGHT - 50, WIDTH - 100, 20))
    pygame.draw.rect(screen, BLUE, (50, HEIGHT - 50, progress * (WIDTH - 100) // 4, 20))

def animate_entry():
    x_pos = -150
    while x_pos < 50:
        screen.fill(WHITE)
        screen.blit(current_female_image, (WIDTH - 200, HEIGHT - 250))
        screen.blit(male_character, (x_pos, HEIGHT - 250))
        pygame.display.flip()
        x_pos += 5
        time.sleep(0.01)

def mini_game():
    global state
    input_active = True
    user_text = ""
    
    while input_active:
        screen.fill(WHITE)
        draw_text("Mini Challenge: What is 2 + 2?", 50, 50)
        draw_text("Enter answer: " + user_text, 50, 100)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state["mini_success"] = (user_text.strip() == "4")
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
    time.sleep(0.5)

def determine_ending():
    if state.get("final_choice") == "Talk to her":
        if state["boundaries"] == "Respect" and state["effort"] == "Work hard" and state["mini_success"]:
            return "Reunion Ending: New beginnings!"
        elif state["boundaries"] == "Push boundaries" and state["effort"] == "Procrastinate":
            return "Secret Ending: Unexpected connection!"
        else:
            return "Bittersweet Ending: Personal growth!"
    else:
        return "Moving Forward: New horizons await!"

def show_ending(message):
    screen.fill(WHITE)
    draw_text(message, 50, 100)
    draw_text("Press any key to exit", 50, 300)
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            return

# Initial animation
animate_entry()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i, choice in enumerate(scenes[scene_index]["choices"]):
                if pygame.Rect(50, 200 + i * 60, 300, 50).collidepoint(x, y):
                    try:
                        click_sound.play()
                    except:
                        pass
                    
                    # Handle choices
                    if scene_index == 1:
                        state["boundaries"] = choice
                        current_female_image = female_images["strict"] if choice == "Push boundaries" else female_images["normal"]
                    elif scene_index == 3:
                        state["effort"] = choice
                    elif scene_index == 4:
                        state["final_choice"] = choice
                        
                    progress += 1
                    scene_index += 1

                    if scene_index == 2:
                        mini_game()
                        progress += 1
                        scene_index += 1

    draw_scene()
    pygame.display.flip()
    
    if scene_index >= len(scenes):
        try:
            success_sound.play()
        except:
            pass
        show_ending(determine_ending())
        running = False

pygame.quit()