import random
import math
import pygame

# Create class asteroid
class Asteroid:
    # Konstruktor der Asteroidklasse, empfängt (x, y, t, gameDisplay, display_width, display_height)
    def __init__(self, x, y, t, gameDisplay, display_width, display_height):
        self.x = x
        self.y = y

        # Größe des Asteroiden bestimmen (Small, Normal, Large)
        if t == "Large":
            self.size = 30
        elif t == "Normal":
            self.size = 20
        else:
            self.size = 10

        self.t = t # Typ des Asteroiden (Small, Normal, Large)
        self.gameDisplay = gameDisplay
        self.display_width = display_width
        self.display_height = display_height

        # Asteroiden Sprite laden
        self.sprite = pygame.image.load("Assets/Asteroid.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.size * 2, self.size * 2))  # Skalieren des Asteroiden Sprites

        # Zufällige Geschwindigkeit und Richtung für den Asteroiden
        self.speed = random.uniform(1, (40 - self.size) * 4 / 15)
        self.dir = random.randrange(0, 360) * math.pi / 180

        # Rotation des Asteroiden
        self.angle = 0
        self.rotation_speed = random.uniform(-1, 1)  # Rotationsgeschwindigkeit

    def updateAsteroid(self):
        # Asteroid bewegen
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)

        # Prüfen ob der Asteroid das Spielfeld verlassen hat
        if self.x > self.display_width:
            self.x = 0
        elif self.x < 0:
            self.x = self.display_width
        if self.y > self.display_height:
            self.y = 0
        elif self.y < 0:
            self.y = self.display_height

        # Rotiere den Asteroiden
        self.angle += self.rotation_speed
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        rect = rotated_sprite.get_rect(center=(self.x, self.y))

        # Male den rotierten Asteroiden auf das Spielfeld
        self.gameDisplay.blit(rotated_sprite, rect.topleft)

