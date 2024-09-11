import random
import pygame

class Particle:
    def __init__(self, x, y, gameDisplay, display_width, display_height):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)  # Random particle size
        self.color = (255, 255, 255)  # White color
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = random.randint(20, 50)  # Particle life span
        self.gameDisplay = gameDisplay
        self.display_width = display_width
        self.display_height = display_height

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1  # Decrease life with each frame
        # Draw the particle
        pygame.draw.circle(self.gameDisplay, self.color, (int(self.x), int(self.y)), self.size)

    def is_alive(self):
        return self.life > 0
