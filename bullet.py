import math
import pygame


# Create class bullet
class Bullet:
    def __init__(self, x, y, direction, gameDisplay, display_width, display_height):
        self.x = x
        self.y = y
        self.dir = direction
        self.life = 30
        self.white = (255, 255, 255)
        self.bullet_speed = 15
        self.gameDisplay = gameDisplay
        self.display_width = display_width
        self.display_height = display_height

    def updateBullet(self):
        # Moving
        self.x += self.bullet_speed * math.cos(self.dir * math.pi / 180)
        self.y += self.bullet_speed * math.sin(self.dir * math.pi / 180)

        # Drawing
        pygame.draw.circle(self.gameDisplay, self.white, (int(self.x), int(self.y)), 3)

        # Wrapping
        if self.x > self.display_width:
            self.x = 0
        elif self.x < 0:
            self.x = self.display_width
        elif self.y > self.display_height:
            self.y = 0
        elif self.y < 0:
            self.y = self.display_height
        self.life -= 1


class RocketBullet(Bullet):
    def __init__(self, x, y, direction, gameDisplay, display_width, display_height, image_file):
        super().__init__(x, y, direction, gameDisplay, display_width, display_height)
        self.image = pygame.image.load(image_file)  # Laden des Raketenbildes
        self.image = pygame.transform.scale(self.image, (20, 40))  # Skalieren des Bildes
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.exploded = False
        self.bullet_speed = 10  # Reduzierte Geschwindigkeit der Rakete

    def updateBullet(self):
        # Bewegen Sie die Rakete
        self.x += self.bullet_speed * math.cos(self.dir * math.pi / 180)
        self.y += self.bullet_speed * math.sin(self.dir * math.pi / 180)

        # Aktualisieren Sie das Rechteck der Rakete
        self.rect.center = (self.x, self.y)

        #Dder Obere Rand des bildes der Rakete soll immer in Schussrichtung zeigen
        rotated_image = pygame.transform.rotate(self.image, -self.dir)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)

        # Zeichnen Sie die Rakete
        self.gameDisplay.blit(rotated_image, rotated_rect.topleft)

        # Wrapping
        if self.x > self.display_width:
            self.x = 0
        elif self.x < 0:
            self.x = self.display_width
        elif self.y > self.display_height:
            self.y = 0
        elif self.y < 0:
            self.y = self.display_height
        self.life -= 1


class ExplosionBullet(Bullet):
    def __init__(self, x, y, direction, gameDisplay, display_width, display_height):
        super().__init__(x, y, direction, gameDisplay, display_width, display_height)
        self.bullet_speed = 10
        self.white = (255, 0, 0)
        self.radius = 5
