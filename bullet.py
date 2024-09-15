import math
import pygame

class Bullet:
    # Konstruktor der Bulletklasse, empfängt (x, y, direction, gameDisplay, display_width, display_height)
    def __init__(self, x, y, direction, gameDisplay, display_width, display_height):
        self.x = x
        self.y = y
        self.dir = direction
        self.life = 30
        self.color = (255, 255, 255) # Farbe der Kugel in weiß (RGB)
        self.bullet_speed = 15
        self.gameDisplay = gameDisplay
        self.display_width = display_width
        self.display_height = display_height

    def updateBullet(self):
        # Bewegung der Kugel
        self.x += self.bullet_speed * math.cos(self.dir * math.pi / 180)
        self.y += self.bullet_speed * math.sin(self.dir * math.pi / 180)

        self.drawBullet()

        # Prüfen ob die Kugel das Spielfeld verlassen hat
        if self.x > self.display_width:
            self.x = 0
        elif self.x < 0:
            self.x = self.display_width
        elif self.y > self.display_height:
            self.y = 0
        elif self.y < 0:
            self.y = self.display_height
        self.life -= 1

    # Zeichnet die Kugel
    def drawBullet(self):
        pygame.draw.circle(self.gameDisplay, self.color, (int(self.x), int(self.y)), 3)


class RocketBullet(Bullet):

    # Konstruktor der RocketBulletklasse, empfängt (x, y, direction, gameDisplay, display_width, display_height)
    def __init__(self, x, y, direction, gameDisplay, display_width, display_height):
        super().__init__(x, y, direction, gameDisplay, display_width, display_height)
        self.bullet_speed = 10  # Reduzierte Geschwindigkeit der Rakete
        self.flame_colors = [(255, 255, 0), (255, 165, 0), (255, 0, 0)]  # Gelb, Orange, Rot für die Flamme

    def drawBullet(self):
        # Zeichnen Sie die Rakete
        projectile_length = 20
        projectile_width = 5
        end_x = self.x + projectile_length * math.cos(math.radians(self.dir))
        end_y = self.y + projectile_length * math.sin(math.radians(self.dir))
        pygame.draw.line(self.gameDisplay, (0, 0, 0), (self.x, self.y), (end_x, end_y), projectile_width)

        # Zeichnen der Flamme
        flame_length = 15
        flame_width = 3
        flame_end_x = self.x - flame_length * math.cos(math.radians(self.dir))
        flame_end_y = self.y - flame_length * math.sin(math.radians(self.dir))
        for color in self.flame_colors:
            pygame.draw.line(self.gameDisplay, color, (self.x, self.y), (flame_end_x, flame_end_y), flame_width)
            flame_length -= 5  # Verkleinere die Flamme für den nächsten Farbabschnitt


# Erstellt eine ExplosionBulletklasse, die von der Bulletklasse erbt
class ExplosionBullet(Bullet):
    # Konstruktor der ExplosionBulletklasse, empfängt (x, y, direction, gameDisplay, display_width, display_height)
    def __init__(self, x, y, direction, gameDisplay, display_width, display_height):
        super().__init__(x, y, direction, gameDisplay, display_width, display_height)
        self.bullet_speed = 10
        self.white = (255, 0, 0)
        self.radius = 5
