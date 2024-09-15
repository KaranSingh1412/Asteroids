import math
import random
import pygame

from bullet import Bullet

# Ufo Klasse
class Saucer:
    # Konstruktor der Saucerklasse, empfängt (display_width, display_height, gameDisplay)
    def __init__(self, display_width, display_height, gameDisplay):
        self.x = 0
        self.y = 0
        self.state = "Dead"
        self.type = "Large"
        self.dirchoice = ()
        self.bullets = []
        self.cd = 0 # Cooldown für Schüsse
        self.bdir = 0
        self.soundDelay = 0
        self.gameDisplay = gameDisplay
        self.display_width = display_width
        self.display_height = display_height
        self.saucer_speed = 5
        self.snd_saucerB = pygame.mixer.Sound("Sounds/saucerBig.wav")
        self.snd_saucerS = pygame.mixer.Sound("Sounds/saucerSmall.wav")

        # Lautstärke von Ufo Sounds anpassen
        self.snd_saucerB.set_volume(0.5)
        self.snd_saucerS.set_volume(0.5)

        # Ufo Sprite laden
        self.saucer_image_original = pygame.image.load("Assets/saucer.png")

        # Ufo Sprite skalieren basierend auf der Größe
        self.saucer_image_large = pygame.transform.scale(self.saucer_image_original, (50, 29))
        self.saucer_image_small = pygame.transform.scale(self.saucer_image_original, (25, 14))

    def updateSaucer(self):
        # Saucer bewegen
        self.x += self.saucer_speed * math.cos(self.dir * math.pi / 180)
        self.y += self.saucer_speed * math.sin(self.dir * math.pi / 180)

        # Zufällige Richtung in die das Ufo fliegt
        if random.randrange(0, 100) == 1:
            self.dir = random.choice(self.dirchoice)

        # Schauen ob das Ufo das Spielfeld verlassen hat
        if self.y < 0:
            self.y = self.display_height
        elif self.y > self.display_height:
            self.y = 0
        if self.x < 0 or self.x > self.display_width:
            self.state = "Dead"

        # Ufo Schüsse
        if self.cd == 0:
            self.bullets.append(Bullet(self.x, self.y, self.bdir, self.gameDisplay, self.display_width, self.display_height))
            self.cd = 30
        else:
            self.cd -= 1

        # Play SFX
        if self.type == "Large":
            pygame.mixer.Sound.play(self.snd_saucerB)
        else:
            pygame.mixer.Sound.play(self.snd_saucerS)

    def createSaucer(self):
        # Ufo erstellen
        self.state = "Alive"

        # Zufällige Position des Ufos
        self.x = random.choice((0, self.display_width))
        self.y = random.randint(0, self.display_height)

        # Zufällige Größe des Ufos
        if random.randint(0, 1) == 0:
            self.type = "Large"
            self.size = 50  # Size for half-sized large saucer
        else:
            self.type = "Small"
            self.size = 25  # Size for half-sized small saucer

        # Zufällige Richtung des Ufos
        if self.x == 0:
            self.dir = 0
            self.dirchoice = (0, 45, -45)
        else:
            self.dir = 180
            self.dirchoice = (180, 135, -135)

        self.cd = 0

    def drawSaucer(self):
        if self.state == "Alive":
            if self.type == "Large":
                # Rotierter halbgroßer großer Ufo Sprite
                rotated_saucer = pygame.transform.rotate(self.saucer_image_large, -self.dir)
            else:
                # Rotierter halbgroßer kleiner Ufo Sprite
                rotated_saucer = pygame.transform.rotate(self.saucer_image_small, -self.dir)

            saucer_rect = rotated_saucer.get_rect(center=(self.x, self.y))
            self.gameDisplay.blit(rotated_saucer, saucer_rect)
