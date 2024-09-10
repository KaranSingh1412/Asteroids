import math
import pygame

# Class player
class Player:
    def __init__(self, x, y, gameDisplay, display_width, display_height, player_size):
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.dir = -90
        self.rtspd = 0
        self.thrust = False
        self.radius = 5
        self.gameDisplay = gameDisplay
        self.display_width = display_width
        self.display_height = display_height
        self.fd_fric = 0.5
        self.bd_fric = 0.1
        self.player_max_speed = 20
        self.player_size = player_size
        self.white = (255, 255, 255)
        self.active_powerups = []

    def updatePlayer(self):
        # Move player
        speed = math.sqrt(self.hspeed**2 + self.vspeed**2)
        if self.thrust:
            if speed + self.fd_fric < self.player_max_speed:
                self.hspeed += self.fd_fric * math.cos(self.dir * math.pi / 180)
                self.vspeed += self.fd_fric * math.sin(self.dir * math.pi / 180)
            else:
                self.hspeed = self.player_max_speed * math.cos(self.dir * math.pi / 180)
                self.vspeed = self.player_max_speed * math.sin(self.dir * math.pi / 180)
        else:
            if speed - self.bd_fric > 0:
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
        a = math.radians(self.dir)
        x = self.x
        y = self.y
        s = self.player_size
        t = self.thrust
        # Draw player
        pygame.draw.line(self.gameDisplay, self.white,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + a),
                          y - (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(self.gameDisplay, self.white,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - a),
                          y + (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(self.gameDisplay, self.white,
                         (x - (s * math.sqrt(2) / 2) * math.cos(a + math.pi / 4),
                          y - (s * math.sqrt(2) / 2) * math.sin(a + math.pi / 4)),
                         (x - (s * math.sqrt(2) / 2) * math.cos(-a + math.pi / 4),
                          y + (s * math.sqrt(2) / 2) * math.sin(-a + math.pi / 4)))
        if t:
            pygame.draw.line(self.gameDisplay, self.white,
                             (x - s * math.cos(a),
                              y - s * math.sin(a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(a + math.pi / 6),
                              y - (s * math.sqrt(5) / 4) * math.sin(a + math.pi / 6)))
            pygame.draw.line(self.gameDisplay, self.white,
                             (x - s * math.cos(-a),
                              y + s * math.sin(-a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(-a + math.pi / 6),
                              y + (s * math.sqrt(5) / 4) * math.sin(-a + math.pi / 6)))

    def killPlayer(self):
        # Reset the player
        self.x = self.display_width / 2
        self.y = self.display_height / 2
        self.thrust = False
        self.dir = -90
        self.hspeed = 0
        self.vspeed = 0
