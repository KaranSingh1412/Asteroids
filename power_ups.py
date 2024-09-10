import pygame
import math


class PowerUps:
    def __init__(self, x, y, duration, name):
        self.x = x
        self.y = y
        self.active = False
        self.timer = 0
        self.radius = 20
        self.image = None
        self.duration = duration
        self.name = name

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def collides_with_player(self, player):
        # Einfache Kollisionsdetektion basierend auf der Entfernung zwischen den Objekten
        distance = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
        return distance < self.radius + player.radius

    def activate(self):
        if self.active:
            # Wenn das Power-Up bereits aktiv ist, erhöhen Sie den Timer um die Dauer
            self.timer += self.duration

        else:
            # Wenn das Power-Up noch nicht aktiv ist, aktivieren Sie es und setzen Sie den Timer
            self.active = True
            self.timer = pygame.time.get_ticks() + self.duration
            print(f"{self.name} aktiviert")
            # Setzen Sie den Timer auf die aktuelle Zeit plus die Dauer

    def update(self):
        if self.active:
            # Überprüfen Sie, ob die aktuelle Zeit größer oder gleich dem Timer ist
            if pygame.time.get_ticks() >= self.timer:
                self.deactivate()
                print(f"{self.name} deaktiviert")

    def deactivate(self):
        self.active = False


class Shield(PowerUps):
    def __init__(self, x, y, image_file, ):
        super().__init__(x, y, 8000, 'Schild')  # Rufen Sie den Konstruktor der Basisklasse auf
        self.is_activated = False
        self.image = pygame.image.load(image_file)  # Laden Sie das Bild

    def activate(self):
        super().activate()  # Rufen Sie die ursprüngliche activate-Methode auf
        self.is_activated = True

    def update(self):
        super().update()


class Rocket(PowerUps):
    def __init__(self, x, y, image_file):
        super().__init__(x, y, 8000, 'Rocket')
        self.is_activated = False
        self.image = pygame.image.load(image_file)

    def activate(self):
        super().activate()
        self.is_activated = True

    def update(self):
        super().update()
