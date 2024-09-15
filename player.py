import math
import pygame

# Eine Klasse für den Spieler
class Player:
    # Konstruktor der Playerklasse, empfängt (x, y, gameDisplay, display_width, display_height, player_size)
    def __init__(self, x, y, gameDisplay, display_width, display_height, player_size):
        self.x = x
        self.y = y
        self.hspeed = 0 # Geschwindigkeit in x-Richtung
        self.vspeed = 0 # Geschwindigkeit in y-Richtung
        self.dir = -90
        self.rtspd = 0 # Rotationsgeschwindigkeit
        self.thrust = False # Schub
        self.radius = 5
        self.gameDisplay = gameDisplay 
        self.display_width = display_width
        self.display_height = display_height
        self.fd_fric = 0.5 # Vorwärtsbeschleunigung
        self.bd_fric = 0.5 # Rückwärtsbeschleunigung
        self.player_max_speed = 20
        self.player_size = player_size
        self.white = (255, 255, 255)
        self.active_powerups = []

        # Raumschiff Sprite laden und höher skalieren
        self.sprite = pygame.image.load('Assets/spaceship.png')
        scaled_size = int(self.player_size * 2)
        self.sprite = pygame.transform.scale(self.sprite, (scaled_size, scaled_size))

    def updatePlayer(self):
        # Spieler bewegen
        speed = math.sqrt(self.hspeed**2 + self.vspeed**2)
        if self.thrust:
            # Beschleunigung in x- und y-Richtung wenn der Spieler beschleunigt
            if speed + self.fd_fric < self.player_max_speed:
                self.hspeed += self.fd_fric * math.cos(self.dir * math.pi / 180)
                self.vspeed += self.fd_fric * math.sin(self.dir * math.pi / 180)
            else:
                self.hspeed = self.player_max_speed * math.cos(self.dir * math.pi / 180)
                self.vspeed = self.player_max_speed * math.sin(self.dir * math.pi / 180)
        else:
            if speed - self.bd_fric > 0:
                # Abbremsen des Spielers, sobald der Spieler aufhört zu beschleunigen
                change_in_hspeed = (self.bd_fric * math.cos(self.vspeed / self.hspeed))
                change_in_vspeed = (self.bd_fric * math.sin(self.vspeed / self.hspeed))
                if self.hspeed != 0:
                    if change_in_hspeed / abs(change_in_hspeed) == self.hspeed / abs(self.hspeed):
                        self.hspeed -= change_in_hspeed
                    else:
                        self.hspeed += change_in_hspeed
                if self.vspeed != 0:
                    if change_in_vspeed / abs(change_in_vspeed) == self.vspeed / abs(self.vspeed):
                        self.vspeed -= change_in_vspeed
                    else:
                        self.vspeed += change_in_vspeed
            else:
                self.hspeed = 0
                self.vspeed = 0
        self.x += self.hspeed
        self.y += self.vspeed

        # Check for wrapping
        if self.x > self.display_width:
            self.x = 0
        elif self.x < 0:
            self.x = self.display_width
        elif self.y > self.display_height:
            self.y = 0
        elif self.y < 0:
            self.y = self.display_height

        # Rotate player
        self.dir += self.rtspd

    def drawPlayer(self):
        # Rotiere das Raumschiff in die jeweilige Richtung
        rotated_sprite = pygame.transform.rotate(self.sprite, -self.dir - 90)
        sprite_rect = rotated_sprite.get_rect(center=(self.x, self.y))
        
        # Spieler zeichnen
        self.gameDisplay.blit(rotated_sprite, sprite_rect.topleft)

    def killPlayer(self):
        # Spieler zurücksetzen, wenn er stirbt
        self.x = self.display_width / 2
        self.y = self.display_height / 2
        self.thrust = False
        self.dir = -90
        self.hspeed = 0
        self.vspeed = 0
