import tkinter as tk
import random
import sys

WIDTH = 800
HEIGHT = 600
PLAYER_SIZE = 50
ENEMY_SIZE = 40
PLAYER_SPEED = 10
ENEMY_SPEED = 5
SPAWN_DELAY = 30

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Kurulus Osman")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.player = self.canvas.create_rectangle(WIDTH//2 - PLAYER_SIZE//2, HEIGHT - PLAYER_SIZE - 10,
                                                   WIDTH//2 + PLAYER_SIZE//2, HEIGHT - 10, fill="blue")
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.game_over = False
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="white",
                                                   font=("Arial", 24), text="Score: 0")
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.game_loop()

    def move_left(self, event):
        if not self.game_over:
            self.canvas.move(self.player, -PLAYER_SPEED, 0)
            pos = self.canvas.coords(self.player)
            if pos[0] < 0:
                self.canvas.move(self.player, -pos[0], 0)

    def move_right(self, event):
        if not self.game_over:
            self.canvas.move(self.player, PLAYER_SPEED, 0)
            pos = self.canvas.coords(self.player)
            if pos[2] > WIDTH:
                self.canvas.move(self.player, WIDTH - pos[2], 0)

    def spawn_enemy(self):
        x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy = self.canvas.create_rectangle(x, -ENEMY_SIZE, x + ENEMY_SIZE, 0, fill="red")
        self.enemies.append(enemy)

    def move_enemies(self):
        for enemy in self.enemies[:]:
            self.canvas.move(enemy, 0, ENEMY_SPEED)
            pos = self.canvas.coords(enemy)
            if pos[1] > HEIGHT:
                self.canvas.delete(enemy)
                self.enemies.remove(enemy)
                self.score += 1
                self.canvas.itemconfigure(self.score_text, text="Score: " + str(self.score))

    def check_collisions(self):
        player_pos = self.canvas.coords(self.player)
        for enemy in self.enemies:
            enemy_pos = self.canvas.coords(enemy)
            if self.rect_overlap(player_pos, enemy_pos):
                self.game_over = True
                self.end_game()
                break

    def rect_overlap(self, r1, r2):
        if r1[2] < r2[0] or r1[0] > r2[2]:
            return False
        if r1[3] < r2[1] or r1[1] > r2[3]:
            return False
        return True

    def end_game(self):
        over_text = self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over", fill="yellow",
                                              font=("Arial", 48))
        restart_text = self.canvas.create_text(WIDTH//2, HEIGHT//2 + 60, text="Press R to Restart", fill="white",
                                                 font=("Arial", 24))
        self.root.bind("<r>", self.restart)

    def restart(self, event):
        self.canvas.delete("all")
        self.enemies = []
        self.score = 0
        self.player = self.canvas.create_rectangle(WIDTH//2 - PLAYER_SIZE//2, HEIGHT - PLAYER_SIZE - 10,
                                                   WIDTH//2 + PLAYER_SIZE//2, HEIGHT - 10, fill="blue")
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="white",
                                                   font=("Arial", 24), text="Score: 0")
        self.root.unbind("<r>")
        self.game_loop()

    def game_loop(self):
        if not self.game_over:
            self.spawn_timer += 1
            if self.spawn_timer >= SPAWN_DELAY:
                self.spawn_enemy()
                self.spawn_timer = 0
            self.move_enemies()
            self.check_collisions()
            self.root.after(50, self.game_loop)
        else:
            return

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()















































































































































































































































































































































































































































































































































































































































































































































































































































































