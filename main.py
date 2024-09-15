import math
import os
import random
import threading
import webbrowser  # zum sharen des highscores per mail
import time
import json

import pygame

from particle import Particle
import power_ups
from asteroid import Asteroid
from bullet import Bullet
from bullet import RocketBullet
from deadplayer import DeadPlayer
from player import Player
from power_ups import Rocket
from power_ups import Shield
from saucer import Saucer
from bullet import ExplosionBullet
from server import AsteroidsServer

pygame.init()
# game music mixer
pygame.mixer.init()
clock = pygame.time.Clock()

# Initialize constants
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# fenstergröße in pixel
display_width = 1200
display_height = 800

# Spieler größe und max. rotationsgeschwindigkeit
player_size = 15
player_max_rtspd = 10

# Ufo Schussgenauigkeiten für kleine und große Ufos
small_saucer_accuracy = 10
large_saucer_accuracy = 5

# buttongröße für das menü in pixel
button_width = 320
button_height = 50

# hiermit wird das game fenster aufgebaut
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_mode((display_width, display_height), pygame.DOUBLEBUF)
pygame.display.set_caption("Spaceroids")
timer = pygame.time.Clock()

# funktion die den highscore zum vergleichen und anzeigen aus der datei ausließt
def read_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            return int(file.read())
    return 0


# funktion die den neuen highscore (funktion zum überprüfen weiter unten) in die highscore.txt schreibt
def write_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# funktion die die highscore datei löscht, sobalt der user das game schließt
def reset_high_score():
    if os.path.exists("highscore.txt"):
        os.remove("highscore.txt")
    else:
        write_high_score(0)


# Import der sound effekte und musik
snd_fire = pygame.mixer.Sound("Sounds/fire.wav")
snd_bangL = pygame.mixer.Sound("Sounds/bangLarge.wav")
snd_bangM = pygame.mixer.Sound("Sounds/bangMedium.wav")
snd_bangS = pygame.mixer.Sound("Sounds/bangSmall.wav")
snd_extra = pygame.mixer.Sound("Sounds/extra.wav")
menu_music = pygame.mixer.Sound("Music/1.IntoTheSpaceship.wav")
collision_sound = pygame.mixer.Sound("Sounds/Collision.A.wav")
rocket_expl = pygame.mixer.Sound("Sounds/Rocket.Expl.wav")
rocket_start = pygame.mixer.Sound("Sounds/Rocket_start.wav")
Powerupactive = pygame.mixer.Sound("Sounds/Powerupactive.wav")

# Lautstärken von Powerup und Menü sounds anpassen
Powerupactive.set_volume(0.5)
menu_music.set_volume(0.8)

# Import Hintergrundbild für das Menü
background_image = pygame.image.load(
    'Assets/backgrounds/1920-space-wallpaper-banner-background-stunning-view-of-a-cosmic-galaxy-with-planets-and-space-objects-elements-of-this-image-furnished-by-nasa-generate-ai.jpg')
    # danke an Vecteezy.com und den User ahasanaraakter für das bereitstellen dieses Bildes
background_x = 0
background_y = 0
scroll_speed = 1
scroll_direction = -1

# hiermit wird erreicht, dass das Hintergrundbild im Menü sich dynamisch von links nach rechts bewegt mit dem scroll speed 1
def update_scrolling_background():
    global background_x, background_y, scroll_direction

    # Hintergrundbild scrollen abhängig vom der scroll_speed und scroll_direction
    background_x -= scroll_speed * scroll_direction

    # Prüfen ob das Bild den Rand erreicht hat
    if background_x <= -background_image.get_width() + display_width:
        # Linker Rand erreicht, Richtung umkehren
        scroll_direction = -1
        background_x = -background_image.get_width() + display_width
    elif background_x >= 0:
        # Rechter Rand erreicht, Richtung umkehren
        scroll_direction = 1
        background_x = 0

    # Hintergrundbild zeichnen
    gameDisplay.blit(background_image, (int(background_x), int(background_y)))


# Create Helper function to draw texts
def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
    if center:
        rect = screen_text.get_rect()
        rect.center = (x, y)
    else:
        rect = (x, y)
    gameDisplay.blit(screen_text, rect)


# Funktion um Start und Stop der Musik zu verwalten
def handle_menu_music(gameState):
    if gameState in ["Menu", "Multiplayer", "Paused", "Game Over"]:
        if not pygame.mixer.get_busy():
            menu_music.play(-1)  # -1 bedeutet unendlich
    else:
        menu_music.stop()

# Eine Extra Kolliosionsfunktion für die Ufos, da diese Kreisförmig sind
def isCollidingSaucer(x1, y1, x2, y2, r1, r2):
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance < (r1 + r2)

# Eine Kollisionsfunktion für alle anderen Entitäten
def isColliding(x, y, xTo, yTo, size):
    if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size:
        return True
    return False

# funktion um das Start Menü zu zeichnen, 3 Buttons, clickable
def draw_menu_screen():
    update_scrolling_background()
    buttons = []
    button_y_start = display_height / 2 - 1.5 * button_height
    for i, button_text in enumerate(["Play (Enter)", "Remote Controlled (c)", "Quit"]):
        button_x = display_width / 2 - button_width / 2
        button_y = button_y_start + i * (button_height + 10)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(gameDisplay, white, button_rect, 2)
        drawText(button_text, white, display_width / 2, button_y + button_height / 2, 30)
        buttons.append({"text": button_text, "rect": button_rect})
    return buttons

# Funktion um eine Socket Verbindung aufzubauen falls der User die App öffnet
def draw_connection_menu(server):
    update_scrolling_background()

    #prüfen ob eine Verbindung besteht und wenn ja, anzeigen welcher Client (App) verbunden ist
    if server.hasConnection:
        drawText(f"Connected to {server.connectedClient}", white, display_width / 2, display_height / 2, 50)
    else:
        # Anzeigen der IP Adresse und des Ports, auf dem der Server läuft damit man sich über die App verbinden kann
        drawText("Waiting for connection...", white, display_width / 2, display_height / 2 - 50, 50)
        drawText(f"IP Address: {server.get_local_ip()}", white, display_width / 2, display_height / 2 + 50, 40)
        drawText(f"Port: {server.TCP_PORT}", white, display_width / 2, display_height / 2 + 100, 40)

    # Button am unteren Bildschirmrand um zurück ins Menü zu gelangen (nicht clickable)
    button_y = display_height - button_height - 20
    button_x = display_width / 2 - button_width / 2
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(gameDisplay, white, button_rect, 2)
    drawText('Back (b)', white, display_width / 2, button_y + button_height / 2, 30)

# Funktion um einen Thread zu starten, damit der Server im Hintergrund läuft
# und nicht den Main Thread blockiert (Führt zu einem eingefrorenen Bildschirm)
def start_server_thread(server):
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()

# Funktion um das Pause Menü zu zeichnen, 3 Buttons, und darüber eine Anzeige über den jetzigen Score
def draw_pause_menu(score):
    update_scrolling_background()
    # Buttons zeichnen
    buttons = []
    button_y_start = display_height / 2 - 1.5 * button_height
    # 3 Buttons zeichnen
    for i, button_text in enumerate(["Resume (esc)", "Retry", "Menu"]):
        button_x = display_width / 2 - button_width / 2
        button_y = button_y_start + i * (button_height + 10)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(gameDisplay, white, button_rect, 2)
        drawText(button_text, white, display_width / 2, button_y + button_height / 2, 30)
        buttons.append({"text": button_text, "rect": button_rect})

    # Aktuellen Score anzeigen
    drawText("Current Score: " + str(score), white, display_width / 2, button_y_start - 50, 30)

    return buttons

# Funktion um das Game Over Menü zu zeichnen, wieder 3 Buttons und Anzeige von Score und Highscore
def draw_game_over_menu(score, high_score):
    update_scrolling_background()
    buttons = []
    button_y_start = display_height / 2 + 50

    #Score und Highscore anzeigen
    drawText(f"High Score: {high_score}", white, display_width / 2, display_height / 2 - 180, 50)
    drawText(f"Your Score: {score}", white, display_width / 2, display_height / 2 - 120, 50)
    # "Game Over" anzeigen
    drawText("Game Over", white, display_width / 2, display_height / 2 - 50, 100)

    # 3 Buttons zeichnen
    button_texts = ["Retry (r)", "Share High Score", "Quit"]
    for i, button_text in enumerate(button_texts):
        button_x = display_width / 2 - button_width / 2
        button_y = button_y_start + i * (button_height + 10)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(gameDisplay, white, button_rect, 2)
        drawText(button_text, white, display_width / 2, button_y + button_height / 2, 30)
        buttons.append({"text": button_text, "rect": button_rect})

    return buttons

# Funktion die bestimmt was beim click auf welchen Button passieren soll,
# welcher gamestate aktiviert wird oder welche funktion getriggert werden soll
def handle_button_click(button_text, score):
    if button_text == "Resume (esc)":
        return "Playing"
    elif button_text == "Retry":
        return "Restart"
    elif button_text == "Share High Score":
        share_high_score(score)
        return None
    elif button_text == "Menu":
        reset_high_score()
        return "Menu"
    elif button_text == "Remote Controlled (c)":
        return "Remote"
    elif button_text == "Quit":
        reset_high_score()
        return "Exit"
    elif button_text == "Play (Enter)":
        return "Playing"
    return None

# funktion um den aktuellen highscore (aus highscore.txt) in eine email mit formuliertem Text und Betreff einzufügen
def share_high_score(score):
    subject = "Schaue dir meinen neunen Spaceroids high score an!"
    body = f"Heyho,\n\nIch habe einen neuen high score von {score} in in meinem neuen Lieblingsretro-game Spaceroids erreicht. Gehe auf https://github.com/KaranSingh1412/Asteroids und versuche ihn zu schlagen :) \n\nViel Erfolg!"
    mailto_link = f"mailto:?subject={subject}&body={body}"
    webbrowser.open(mailto_link)

# Die Main Game Loop Funktion, die das Spiel steuert
def gameLoop(startingState):
    # Init variables
    global power_up
    gameState = startingState
    # Spieler Variablen
    player_state = "Alive"
    player_blink = 0 # Blinking effect nach dem Respawn
    player_pieces = [] # Spielerstücke nach dem Tod (Effekt)
    player_dying_delay = 0 # Delay nach dem Tod
    player_invi_dur = 0 # Unsterblichkeitsdauer nach dem Respawn
    player = Player(display_width / 2, display_height / 2, gameDisplay, display_width, display_height, player_size) # Spieler Objekt

    bullet_capacity = 4 # Maximale Anzahl an Kugeln gleichzeitig
    bullets = [] # Liste aller Kugeln
    particles = [] # Liste aller Partikel (Schusseffekt)
    asteroids = [] # Liste aller Asteroiden
    Explosion_bullets = [] # Liste aller Explosionsbullets (nach Raketenabschuss)
    powerups = [] # Liste aller gespawnten Powerups

    next_level_delay = 0 # Delay nach dem Abschluss eines Levels
    stage = 3 # Aktuelles Level
    score = 0 # Aktueller Score
    live = 2 # Anzahl an Leben (Leben <= 0 -> Game Over)

    oneUp_multiplier = 1 # Multiplikator für die Berechnung des Extra Leben (1 Leben pro 10.000 Punkte)
    hyperspace = 0 # Hyperspace Effekt (Teleportation)
    playOneUpSFX = 0 # Soundeffekt für das Extra Leben
    intensity = 0 # Schwierigkeit des Spiels

    saucer = Saucer(display_width, display_height, gameDisplay) # Ufo Objekt
    high_score = read_high_score() # Highscore auslesen
    last_rocket_shot_time = 0 # Zeitpunkt des letzten Raketenabschusses
    server = None # Server Objekt für Remote Control

    # Main loop
    while gameState != "Exit":
        handle_menu_music(gameState)
        # Game menu
        # bestimmt, was bei jeweiligen shortcuts oder buttonclicks im startmenü passieren soll (funktion oder neuer gamestate)
        while gameState == "Menu":
            buttons = draw_menu_screen()
            handle_menu_music(gameState)
            for event in pygame.event.get(): # Event handling
                if event.type == pygame.QUIT:
                    reset_high_score()
                    gameState = "Exit"
                if event.type == pygame.KEYDOWN:
                    # Wenn Enter gedrückt wird, startet das Spiel - Genauer gesagt beendet dies die aktuelle Spielschleife und startet eine neue, was effektiv einem Neustart des Spiels entspricht. (Bug Fixing wenn vorher schon spiel gespielt, im Pause Menü auf Menu geklickt wurde und dann wieder auf Play geklickt wird)
                    if event.key == pygame.K_RETURN:
                        gameState = "Exit"
                        gameLoop("Playing")
                        handle_menu_music(gameState)
                    # Wenn c gedrückt wird, startet der Server für das Remote Control
                    if event.key == pygame.K_c:
                        gameState = "Remote"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Überprüfen, ob ein Button angeklickt wurde mithilfe der Maus Position
                    mouse_pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            # Ändere den gameState basierend auf dem angeklickten Button
                            if button["text"] == "Play (Enter)":
                            # Auch hier fügen wir die "Retry"-Funktionalität hinzu
                              gameState = "Exit"
                              gameLoop("Playing")
                            elif button["text"] == "Remote Controlled (c)":
                                gameState = "Remote"
                            elif button["text"] == "Quit":
                                reset_high_score()
                                gameState = "Exit"
                                
            pygame.display.update()
            timer.tick(5)
        
        if gameState == "Remote":
            if not server:
                # Prüfe ob der Server bereits gestartet wurde
                server = AsteroidsServer()
                start_server_thread(server) # Starte den Server in einem eigenen Thread

            while gameState == "Remote":
                draw_connection_menu(server) # Zeichne das entsprechende Menü
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        reset_high_score()
                        gameState = "Exit"
                        server.stop_server()
                    if event.type == pygame.KEYDOWN:
                        # Wenn b gedrückt wurde dann geh zurück ins menu und stoppe den server
                        if event.key == pygame.K_b:
                            gameState = "Menu"
                            handle_menu_music(gameState)
                            server.stop_server()

                if server and server.hasConnection:
                    if server.received_data:
                        # Überprüfen ob der Server eine Verbindung hat und Daten empfangen hat
                        if server.received_data == "Play": # Wenn der Controller "Play" sendet, starte das Spiel
                            gameState = "Playing"
                            server.send_signal("Done")
                            server.received_data = None
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        if server:
                            server.stop_server()
                        gameState = "Exit"

                pygame.display.update()
                timer.tick(5)

        # highscore checker überprüft ob highscore überschritten wird und schreibt ggf. neuen score in txt datei
        if score > high_score:
            high_score = score
            write_high_score(high_score)

        # User inputs: wenn quit, dann wird highscore geresetet, wenn esc oder p gedrückt wechselt gamestate auf paused oder playing und die dementsprechende musik wird gespielt/ nicht gespielt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reset_high_score() 
                gameState = "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    if gameState == "Playing":
                        gameState = "Paused"
                    elif gameState == "Paused":
                        gameState = "Playing"
                    # start menu music
                    handle_menu_music(gameState)

                rocket_active = None

                # Die Steuerung des Spielers
                if event.key == pygame.K_UP:
                    # Wenn die obere Pfeiltaste gedrückt wird, aktiviere den Schub
                    player.thrust = True
                elif event.key == pygame.K_LEFT:
                    # Wenn die linke Pfeiltaste gedrückt wird, drehe das Raumschiff nach links
                    player.rtspd = -player_max_rtspd
                elif event.key == pygame.K_RIGHT:
                    # Wenn die rechte Pfeiltaste gedrückt wird, drehe das Raumschiff nach rechts
                    player.rtspd = player_max_rtspd
                elif event.key == pygame.K_SPACE and player_dying_delay == 0 and len(bullets) < bullet_capacity:
                    # Wenn die Leertaste gedrückt wird und der Spieler nicht tot ist und auch wenn die maximale Anzahl an geschossener Kugeln nicht überschritten wurde,
                    # schieße eine Kugel ab
                    rocket_active = False
                    # Überprüfen, ob ein Raketen-Power-Up aktiv ist
                    for power_up in player.active_powerups:
                        if isinstance(power_up, Rocket) and power_up.active:
                            rocket_active = True
                            break

                    current_time = time.time()
                    if rocket_active and current_time - last_rocket_shot_time >= 1:
                        # Wenn ein Raketen-Power-Up aktiv ist und die Zeit seit dem letzten Raketenabschuss größer als 1 Sekunde ist, schieße eine Rakete ab
                        bullets.append(
                            RocketBullet(player.x, player.y, player.dir, gameDisplay, display_width, display_height))
                        # Spiele den Raketen-Sound ab, wenn eine Rakete abgeschossen wird
                        pygame.mixer.Sound.play(rocket_start)
                        last_rocket_shot_time = current_time  # Aktualisiere die Zeit des letzten Raketenabschusses
                    elif not rocket_active:
                        bullets.append(
                            Bullet(player.x, player.y, player.dir, gameDisplay, display_width, display_height))
                        # Spiele den Bullet-Sound ab, wenn eine normale Bullet abgeschossen wird
                        pygame.mixer.Sound.play(snd_fire)

                # wenn r bei game over gedrückt, startet spiel von vorne (playing) aber kein reset des highscores
                if gameState == "Game Over":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop("Playing")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.thrust = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.rtspd = 0
             
            # Wenn man im Pausenmenü oder im Game Over Menü landet,
            # Wird der gameState je nach Button-Click geändert
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameState == "Paused" or gameState == "Game Over":
                    mouse_pos = pygame.mouse.get_pos()
                    buttons = []
                    if gameState == "Paused":
                        buttons = draw_pause_menu(score)
                    elif gameState == "Game Over":
                        buttons = draw_game_over_menu(score, high_score)
                    elif gameState == "Menu":
                        buttons = draw_menu_screen()
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            pygame.draw.rect(gameDisplay, (255, 255, 255), button["rect"], 2)
                            action = handle_button_click(button["text"], score)
                            # Wenn ein Button angeklickt wurde, Führe eine entsprechende Aktion aus
                            if action == "Playing":
                                gameState = "Playing"
                            elif action == "Restart":
                                gameState = "Exit"
                                gameLoop("Playing")
                            elif action == "Menu":
                                gameState = "Menu"
                            elif action == "Exit":
                                pygame.quit()
                                quit()

        # prüfe ob der Server eine Verbindung hat und ob Daten empfangen wurden
        if server and server.hasConnection:
            if server.received_data:
                # Wenn die empfangenen Daten "move" enthalten, dann aktualisiere die Bewegung und die Rotation des Spielers
                if server.received_data.__contains__("move"):
                    try:
                        # Konvertiere das empfangene JSON in ein Python-Dictionary
                        control_data = json.loads(server.received_data) 
                        move_data = control_data.get('move')
                        # Lese die x und y Bewegung des Joysticks (ein float zwischen -1 und 1 in x und y richtung) aus den empfangenen Daten
                        move_x, move_y = move_data[0], move_data[1]

                        # Berechne die Richtung des Spielers anhand der x und y Bewegung
                        if move_x != 0 or move_y != 0:
                            player.dir = math.degrees(math.atan2(move_y, move_x))
                            player.thrust = True
                            player.fd_fric = 0.2
                            player.bd_fric = 0.2
                        else:
                            player.thrust = False

                        server.received_data = None # Setze die empfangenen Daten auf None, um sie nicht erneut zu verarbeiten
                    except json.JSONDecodeError:
                        print("Error decoding JSON from remote controller")
                # Wenn die empfangenen Daten "shoot" enthalten, schieße eine Kugel ab
                elif server.received_data.__contains__('shoot'):
                    # Überprüfen, ob ein Raketen-Power-Up aktiv ist
                    rocket_active = False
                    for power_up in player.active_powerups:
                        if isinstance(power_up, Rocket) and power_up.active:
                            rocket_active = True
                            break

                    current_time = time.time()
                    if rocket_active and current_time - last_rocket_shot_time >= 1:
                        # Wenn ein Raketen-Power-Up aktiv ist und die Zeit seit dem letzten Raketenabschuss größer als 1 Sekunde ist, schieße eine Rakete ab
                        bullets.append(
                            RocketBullet(player.x, player.y, player.dir, gameDisplay, display_width, display_height))
                        # Spiele den Raketen-Sound ab, wenn eine Rakete abgeschossen wird
                        pygame.mixer.Sound.play(rocket_start)
                        last_rocket_shot_time = current_time  # Aktualisiere die Zeit des letzten Raketenabschusses
                    elif not rocket_active:
                        bullets.append(
                            Bullet(player.x, player.y, player.dir, gameDisplay, display_width, display_height))
                        # Spiele den Bullet-Sound ab, wenn eine normale Bullet abgeschossen wird
                        pygame.mixer.Sound.play(snd_fire)
                    server.received_data = None
        # Update player
        player.updatePlayer()

        # Check ob player unsichtbar ist (nach spawn)
        if player_invi_dur != 0:
            player_invi_dur -= 1
        elif hyperspace == 0:
            player_state = "Alive"

        # Setze Bildschirm zurück
        gameDisplay.fill(black)

        # Pause Menu zeichnen wenn Spiel pausiert
        if gameState == "Paused":
            draw_pause_menu(score)
            pygame.display.update()
            timer.tick(5)
            continue 

        # wenn game over, zeichne game over menu mit aktuellem highscore und buttonfunktionen
        elif gameState == "Game Over":
            update_scrolling_background()
            handle_menu_music(gameState)
            buttons = draw_game_over_menu(score, high_score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    reset_high_score()
                    gameState = "Exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop("Playing")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["text"] == "Retry (r)":
                                gameState = "Exit"
                                gameLoop("Playing")
                            elif button["text"] == "Share High Score":
                                share_high_score(score)
                            elif button["text"] == "Quit":
                                reset_high_score()
                                gameState = "Exit"
            pygame.display.update()
            timer.tick(5)
            continue
        
        # prüfe ob ein Powerup gespawnt ist und wenn ja, zeichne es
        for power_up in powerups:
            power_up.draw(gameDisplay)
            # Überprüfen, ob das Power-Up mit dem Spieler kollidiert
            if power_up.collides_with_player(player): 
                if not power_up.is_activated:  # Überprüfen Sie, ob das Power-Up bereits aktiviert wurde
                    power_up.activate()  # Aktivieren Sie das Power-Up
                    Powerupactive.play() # Spiele den Powerup-Sound ab

                    player.active_powerups.append(power_up)

                    print(player.active_powerups)
                    powerups.remove(power_up)

        for power_up in player.active_powerups.copy():  # Verwenden Sie .copy() um über eine Kopie der Liste zu iterieren
            power_up.update()  # Aktualisieren Sie den Zustand des Power-Ups

            # Überprüfen Sie, ob das Power-Up noch aktiv ist
            if not power_up.active:
                # Wenn das Power-Up nicht mehr aktiv ist, entfernen Sie es aus der Liste
                player.active_powerups.remove(power_up)
            elif isinstance(power_up, power_ups.Shield):
                # Wenn das Schild aktiv ist, zeichnen Sie eine  Umrandung um den Spieler
                pygame.draw.circle(gameDisplay, (173, 216, 250), (int(player.x), int(player.y)), player_size + 10, 2)

        # Kollision des Spielers mit dem Asteroiden prüfen
        for a in asteroids:
            a.updateAsteroid()
            if player_state != "Died":
                if isColliding(player.x, player.y, a.x, a.y, a.size):
                    # Überprüfen Sie, ob ein Schild-Powerup aktiv ist
                    shield_active = False
                    # Überprüfen Sie, ob ein Schild-Powerup aktiv ist
                    for power_up in player.active_powerups:
                        print(f"Überprüfe Power-Up: {power_up.name}, Aktiv: {power_up.active}")  # Debug-Ausgabe
                        if isinstance(power_up, Shield) and power_up.active:
                            shield_active = True
                            break
                    if not shield_active:
                        # Der Spieler stirbt nur, wenn kein Schild aktiv ist
                        # Spieler Fragmente erstellen wenn tot
                        player_pieces.append(
                            DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))),
                                       gameDisplay))
                        player_pieces.append(
                            DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))),
                                       gameDisplay))
                        player_pieces.append(DeadPlayer(player.x, player.y, player_size, gameDisplay))

                        # Spieler töten und zurücksetzen
                        player_state = "Died"
                        player_dying_delay = 30
                        player_invi_dur = 120
                        player.killPlayer()

                        # Leben um eins verringern
                        if live != 0:
                            live -= 1
                        else:
                            gameState = "Game Over"

                        # Split asteroid
                        if a.t == "Large":
                            asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                            asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                            score += 20
                            # Play SFX
                            pygame.mixer.Sound.play(snd_bangL)
                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                            asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                            score += 50
                            # Play SFX
                            pygame.mixer.Sound.play(snd_bangM)
                        else:
                            score += 100
                            # Play SFX
                            pygame.mixer.Sound.play(snd_bangS)
                        asteroids.remove(a)
                    else:
                        # Änder die Bewegungsrichtung des Asteroiden anhand des Aufprallwinkels
                        a.dir = math.atan2(a.y - player.y, a.x - player.x)
                        a.speed = 5
                        a.x += a.speed * math.cos(a.dir)
                        a.y += a.speed * math.sin(a.dir)
                        #Füge einen Sound hinzu
                        pygame.mixer.Sound.play(collision_sound)

        # Update ship fragments
        for f in player_pieces:
            f.updateDeadPlayer()
            if f.x > display_width or f.x < 0 or f.y > display_height or f.y < 0:
                player_pieces.remove(f)

        # Schauen ob man am ende eines Levels angekommen ist
        if len(asteroids) == 0 and saucer.state == "Dead":
            if next_level_delay < 30:
                next_level_delay += 1
            else:
                stage += 1
                intensity = 0
                # Asteroiden um die Mitte herum spawnen
                for i in range(stage):
                    xTo = display_width / 2
                    yTo = display_height / 2
                    while xTo - display_width / 2 < display_width / 4 and yTo - display_height / 2 < display_height / 4:
                        xTo = random.randrange(0, display_width)
                        yTo = random.randrange(0, display_height)
                    asteroids.append(Asteroid(xTo, yTo, "Large", gameDisplay, display_width, display_height))
                next_level_delay = 0

        # Schwierigkeitsgrad erhöhen
        if intensity < stage * 450:
            intensity += 1

        # Totes Ufo neu spawnen
        if saucer.state == "Dead":
            if random.randint(0, 5000) <= (intensity * 3) / (stage * 10) and next_level_delay == 0:
                saucer.createSaucer()
                # Wahrscheinlichkeit für kleine Saucer erhöhen, wenn der Score >= 4000 ist
                if score >= 4000:
                    if random.random() < 0.75:  # 75% Wahrscheinlichkeit für kleine Saucer
                        saucer.type = "Small"
                    else:
                        saucer.type = "Large"
                else:
                    if random.randint(0, 1) == 0:
                        saucer.type = "Small"
                    else:
                        saucer.type = "Large"
        else:
            # Ufo Ausrichtung setzen
            if saucer.type == "Small":
                # Wenn Ufo klein ist, dann ist die Genauigkeit 4 mal so hoch
                acc = small_saucer_accuracy * 4 / stage
            else:
                # Ansonsten ist die Genauigkeit nur 2 mal so hoch
                acc = large_saucer_accuracy * 2 / stage
            saucer.bdir = math.degrees(
                math.atan2(-saucer.y + player.y, -saucer.x + player.x) + math.radians(random.uniform(acc, -acc)))

            # ab 4000 Score sollen sich Ausweichmanöver häufiger vorkommen
            if score >= 1000:
                if random.randint(0, 100) < 50:
                    saucer.bdir = random.randint(0, 360)

            saucer.updateSaucer()
            saucer.drawSaucer()

            # Kollision zwischen Asteroid und Ufo prüfen
            for a in asteroids:
                if isCollidingSaucer(saucer.x, saucer.y, a.x, a.y, saucer.size/2, a.size/2):
                    # Ufo töten
                    saucer.state = "Dead"

                    # Asteroid teilen
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)

            for b in bullets:
                # Killision zwischen Kugel und Ufo prüfen
                if isColliding(b.x, b.y, saucer.x, saucer.y, saucer.size):
                    # Score erhöhen wenn von Spieler Kugel getroffen
                    if saucer.type == "Large":
                        score += 200
                    else:
                        score += 1000

                    # Ufo töten
                    saucer.state = "Dead"

                    # Wählen Sie zufällig ein Power-Up aus
                    power_up_type = random.choice(['Shield', 'Rocket'])

                    if power_up_type == 'Shield':
                        new_power_up = power_ups.Shield(saucer.x, saucer.y, 'Assets/Powerups/Shield.png')
                        powerups.append(new_power_up)
                    elif power_up_type == 'Rocket':
                        new_power_up = power_ups.Rocket(saucer.x, saucer.y, 'Assets/Powerups/Rocket2.png')
                        powerups.append(new_power_up)

                    # Play SFX
                    pygame.mixer.Sound.play(snd_bangL)

                    # Kugel entfernen und Partikel spawnen
                    bullets.remove(b)
                    for _ in range(10):
                        particle = Particle(b.x, b.y, gameDisplay, display_width, display_height)
                        particles.append(particle)

                    # Überprüfen, ob die Kugel eine RocketBullet ist und explodiert
                    if isinstance(b, RocketBullet):
                        # Spielen Sie den Explosionseffekt ab
                        pygame.mixer.Sound.play(rocket_expl)
                        b.exploded = True
                        # Erzeugen Sie kleinere Projektile (normale Bullets) in unterschiedlichen zufälligen Richtungen
                        small_projectiles = []
                        for _ in range(20):  # Anzahl der kleineren Projektile

                            angle = random.uniform(0, 360)

                            small_projectiles.append(
                                ExplosionBullet(b.x, b.y, angle, b.gameDisplay, b.display_width, b.display_height))
                        Explosion_bullets.extend(small_projectiles)  # Verwende die Liste explosion_bullets

            # Kollision zwischen Ufo und Spieler prüfen
            if isColliding(saucer.x, saucer.y, player.x, player.y, saucer.size):
                if player_state != "Died":
                    shield_active = False
                    # Überprüfen Sie, ob ein Schild-Powerup aktiv ist, wenn ja dann passiert nichts
                    for power_up in player.active_powerups:
                        if isinstance(power_up, Shield) and power_up.active:
                            shield_active = True
                            break
                    # Wenn kein Schild aktiv ist, dann stirbt der Spieler
                    if not shield_active:
                        player_pieces.append(
                            DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))),
                                       gameDisplay))
                        player_pieces.append(
                            DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))),
                                       gameDisplay))
                        player_pieces.append(DeadPlayer(player.x, player.y, player_size, gameDisplay))

                        player_state = "Died"
                        player_dying_delay = 30
                        player_invi_dur = 120
                        player.killPlayer()

                        if live != 0:
                            live -= 1
                        else:
                            gameState = "Game Over"

                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangL)
                    # Spieler Fragmente erstellen
                    else:
                        #der Spieler soll nicht sterben und der Colisionsound soll abgespielt werden
                        pygame.mixer.Sound.play(collision_sound)

            # Ufo Kugeln event handling
            for b in saucer.bullets:
                # Update bullets
                b.updateBullet()

                # Kollision zwischen Kugel und Asteroid prüfen
                for a in asteroids:
                    if isColliding(b.x, b.y, a.x, a.y, a.size):
                        # Split asteroid
                        if a.t == "Large":
                            asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                            asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                            # Play SFX
                            pygame.mixer.Sound.play(snd_bangL)
                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                            asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                            # Play SFX
                            pygame.mixer.Sound.play(snd_bangL)
                        else:
                            # Play SFX
                            pygame.mixer.Sound.play(snd_bangL)

                        # Asteroid und Kugel entfernen
                        asteroids.remove(a)
                        saucer.bullets.remove(b)
                        break

                # Kollision zwischen Ufo Kugel und Spieler prüfen
                for b in saucer.bullets:
                    if isColliding(player.x, player.y, b.x, b.y, player.player_size):
                        if player_state != "Died":
                            # Überprüfen Sie, ob ein Schild-Powerup aktiv ist
                            shield_active = False
                            for power_up in player.active_powerups:
                                if isinstance(power_up, Shield) and power_up.active:
                                    shield_active = True
                                    break
                            if not shield_active:
                                # Spieler Fragmente erstellen
                                player_pieces.append(
                                    DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))),
                                               gameDisplay))
                                player_pieces.append(
                                    DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))),
                                               gameDisplay))
                                player_pieces.append(DeadPlayer(player.x, player.y, player_size, gameDisplay))

                                # Spieler zurücksetzen
                                player_state = "Died"
                                player_dying_delay = 30
                                player_invi_dur = 120
                                player.killPlayer()

                                if live != 0:
                                    live -= 1
                                else:
                                    gameState = "Game Over"

                                # Play SFX
                                pygame.mixer.Sound.play(snd_bangL)
                            else:
                                saucer.bullets.remove(b)
                                # füge den Sound coliision_sound hinzu
                                pygame.mixer.Sound.play(collision_sound)

                    if b.life <= 0:
                        try:
                            saucer.bullets.remove(b)
                        except ValueError:
                            continue

        # Kugeln event handling
        for b in bullets:
            # Update bullets
            b.updateBullet()

            # Überprüfen, ob das Rocket-Power-Up aktiv ist
            rocket_active = False
            for power_up in player.active_powerups:
                if isinstance(power_up, Rocket) and power_up.active:
                    rocket_active = True
                    break

            # Wenn das Rocket-Power-Up aktiv ist und die Kugel eine normale Bullet ist, ändern Sie sie in eine RocketBullet
            if rocket_active and isinstance(b, Bullet) and not isinstance(b, RocketBullet):
                rocket_bullet = RocketBullet(b.x, b.y, b.dir, b.gameDisplay, b.display_width, b.display_height)
                bullets.append(rocket_bullet)
                bullets.remove(b)
                b = rocket_bullet

            # Kollision zwischen Kugel und Asteroid prüfen
            for a in asteroids:
                if b.x > a.x - a.size and b.x < a.x + a.size and b.y > a.y - a.size and b.y < a.y + a.size:
                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                        score += 20
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                        score += 50
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)
                    if b in bullets:
                        bullets.remove(b)
                        for _ in range(20):
                            particle = Particle(b.x, b.y, gameDisplay, display_width, display_height)
                            particles.append(particle)

                    # Überprüfen, ob die Kugel eine RocketBullet ist und explodiert
                    if isinstance(b, RocketBullet):
                        # Spielen Sie den Explosionseffekt ab
                        pygame.mixer.Sound.play(rocket_expl)
                        b.exploded = True
                        # Erzeugen Sie kleinere Projektile (normale Bullets) in unterschiedlichen zufälligen Richtungen
                        small_projectiles = []
                        for _ in range(20):  # Anzahl der kleineren Projektile
                            #die Projektile sollen in 10 unterschiiedliche Richtungen fliegen
                            angle = random.uniform(0, 360)

                            small_projectiles.append(
                                ExplosionBullet(b.x, b.y, angle, b.gameDisplay, b.display_width, b.display_height))
                        Explosion_bullets.extend(small_projectiles)  # Verwende die Liste explosion_bullets

                    break

            # Kugel entfernen und Partikel spawnen
            if b.life <= 0:
                for _ in range(10):
                    particle = Particle(b.x, b.y, gameDisplay, display_width, display_height)
                    particles.append(particle)
                try:
                    bullets.remove(b)
                except ValueError:
                    continue

        # Partikel spawnen
        for particle in particles:
            particle.update()
            if not particle.is_alive():
                particles.remove(particle)

        # ExplosionBullets
        for eb in Explosion_bullets:
            # Update explosion bullets
            eb.updateBullet()

            # Kolliosion zwischen Explosionskugel und Asteroid prüfen
            for a in asteroids:
                if eb.x > a.x - a.size and eb.x < a.x + a.size and eb.y > a.y - a.size and eb.y < a.y + a.size:
                    # Split asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                        asteroids.append(Asteroid(a.x, a.y, "Normal", gameDisplay, display_width, display_height))
                        score += 20
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangL)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                        asteroids.append(Asteroid(a.x, a.y, "Small", gameDisplay, display_width, display_height))
                        score += 50
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        score += 100
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)
                    if eb in Explosion_bullets:
                        Explosion_bullets.remove(eb)

            # Explosionskugel entfernen
            if eb.life <= 0:
                try:
                    Explosion_bullets.remove(eb)
                except ValueError:
                    continue

        # Extra leben wenn spieler 10000 punkte erreicht
        if score > oneUp_multiplier * 10000:
            oneUp_multiplier += 1
            live += 1
            playOneUpSFX = 60
        # Play sfx
        if playOneUpSFX > 0:
            playOneUpSFX -= 1
            pygame.mixer.Sound.play(snd_extra, 60)

        # Spieler Animationen und State Handling abhängig davon ob der Spieler tot ist oder nicht
        if gameState != "Game Over":
            if player_state == "Died":
                if hyperspace == 0:
                    if player_dying_delay == 0:
                        if player_blink < 5:
                            if player_blink == 0:
                                player_blink = 10
                            else:
                                player.drawPlayer()
                        player_blink -= 1
                    else:
                        player_dying_delay -= 1
            else:
                player.drawPlayer()

        # score und high score für ingame Anzeige
        drawText(f"Score: {score}", white, 60, 20, 40, False)
        drawText(f"High Score: {high_score}", white, display_width - 350, 20, 40, False)

        # verbleibende Leben, Anzeige ingame
        for l in range(live + 1):
            Player(75 + l * 25, 75, gameDisplay, display_width, display_height, player_size).drawPlayer()

        # Update screen
        pygame.display.update()

        # Tick fps während des Spiels
        clock.tick(30)


# Starte Spiel im gamestate "Menu"
gameLoop("Menu")

# End game
reset_high_score()  # Reset high score wenn script endet / bei quit
pygame.quit()
quit()
