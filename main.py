# Import modules
import os
import pygame
import math
import random
from asteroid import Asteroid
from bullet import Bullet
from deadplayer import DeadPlayer
from player import Player
from saucer import Saucer
import power_ups
import webbrowser # zum sharen des highscores per mail

pygame.init()
# game music mixer
pygame.mixer.init()
clock = pygame.time.Clock()


# Initialize constants
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

display_width = 1200
display_height = 800

player_size = 10
player_max_rtspd = 10

small_saucer_accuracy = 10

# Make surface and display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_mode((display_width, display_height), pygame.DOUBLEBUF)
pygame.display.set_caption("Asteroids")
timer = pygame.time.Clock()

def read_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            return int(file.read())
    return 0

def write_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

def reset_high_score():
    if os.path.exists("highscore.txt"):
        os.remove("highscore.txt")
    else:
        write_high_score(0)
                   
# Import sound effects and music
snd_fire = pygame.mixer.Sound("Sounds/fire.wav")
snd_bangL = pygame.mixer.Sound("Sounds/bangLarge.wav")
snd_bangM = pygame.mixer.Sound("Sounds/bangMedium.wav")
snd_bangS = pygame.mixer.Sound("Sounds/bangSmall.wav")
snd_extra = pygame.mixer.Sound("Sounds/extra.wav")
menu_music = pygame.mixer.Sound("Music/1.IntoTheSpaceship.wav")

# Import Background Image Menu
background_image = pygame.image.load('Assets/backgrounds/1920-space-wallpaper-banner-background-stunning-view-of-a-cosmic-galaxy-with-planets-and-space-objects-elements-of-this-image-furnished-by-nasa-generate-ai.jpg')
background_x = 0
background_y = 0
scroll_speed = 1  # Adjust this value to change the scrolling speed
scroll_direction = 1  # 1 for right to left, -1 for left to right

def update_scrolling_background():
    global background_x, background_y, scroll_direction
    
    # Update the background position
    background_x -= scroll_speed * scroll_direction
    
    # Check if we've reached either end
    if background_x <= -background_image.get_width() + display_width:
        # Reached the left end, reverse direction
        scroll_direction = -1
        background_x = -background_image.get_width() + display_width
    elif background_x >= 0:
        # Reached the right end, reverse direction
        scroll_direction = 1
        background_x = 0
    
    # Draw the background
    gameDisplay.blit(background_image, (int(background_x), int(background_y)))

# Create function to draw texts
def drawText(msg, color, x, y, s, center=True):
    screen_text = pygame.font.SysFont("Calibri", s).render(msg, True, color)
    if center:
        rect = screen_text.get_rect()
        rect.center = (x, y)
    else:
        rect = (x, y)
    gameDisplay.blit(screen_text, rect)

# Create a function to handle playing and stopping the music
def handle_menu_music(gameState):
    if gameState in ["Menu", "Paused", "Game Over"]:
        if not pygame.mixer.get_busy():
            menu_music.play(-1)  # -1 means loop indefinitely
    else:
        menu_music.stop()

# Create function to check for collision
def isColliding(x, y, xTo, yTo, size):
    if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size:
        return True
    return False

def draw_pause_menu(score):
    update_scrolling_background()
    # Draw the buttons
    buttons = []
    button_width = 200
    button_height = 50
    button_y_start = display_height / 2 - 1.5 * button_height
    for i, button_text in enumerate(["Resume (esc)", "Retry (r)", "Quit (q)"]):
        button_x = display_width / 2 - button_width / 2
        button_y = button_y_start + i * (button_height + 10)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(gameDisplay, white, button_rect, 2)
        drawText(button_text, white, display_width / 2, button_y + button_height / 2, 30)
        buttons.append({"text": button_text, "rect": button_rect})

    # Draw the current score
    drawText("Current Score: " + str(score), white, display_width / 2, button_y_start - 50, 30)

    return buttons

def draw_game_over_menu(score, high_score):
    update_scrolling_background()
    buttons = []
    button_width = 200
    button_height = 50
    button_y_start = display_height / 2 + 50

    drawText(f"High Score: {high_score}", white, display_width / 2, display_height / 2 - 180, 50)
    drawText(f"Your Score: {score}", white, display_width / 2, display_height / 2 - 120, 50)
    drawText("Game Over", white, display_width / 2, display_height / 2 - 50, 100)

    button_texts = ["Retry (r)", "Share High Score", "Quit (q)"]
    for i, button_text in enumerate(button_texts):
        button_x = display_width / 2 - button_width / 2
        button_y = button_y_start + i * (button_height + 10)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(gameDisplay, white, button_rect, 2)
        drawText(button_text, white, display_width / 2, button_y + button_height / 2, 30)
        buttons.append({"text": button_text, "rect": button_rect})

    return buttons

def handle_button_click(button_text, score):
    if button_text == "Resume (esc)":
        return "Playing"
    elif button_text == "Retry (r)":
        return "Restart"
    elif button_text == "Share High Score":
        share_high_score(score)
        return None
    elif button_text == "Quit (q)":
        reset_high_score()
        return "Exit"
    return None

def share_high_score(score):
    subject = "Schaue dir meinen neunen Asteroids 2.0 high score an!"
    body = f"Heyho,\n\nIch habe einen neuen high score von {score} in in meinem neuen Lieblingsretro-game Asteroids 2.0 erreicht. Gehe auf https://github.com/KaranSingh1412/Asteroids und versuche ihn zu schlagen :) \n\nViel Erfolg!"
    mailto_link = f"mailto:?subject={subject}&body={body}"
    webbrowser.open(mailto_link)

def gameLoop(startingState):
    # Init variables
    gameState = startingState
    player_state = "Alive"
    player_blink = 0
    player_pieces = []
    player_dying_delay = 0
    player_invi_dur = 0
    next_level_delay = 0
    bullet_capacity = 4
    bullets = []
    asteroids = []
    powerups = []
    active_powerups = []
    stage = 3
    score = 0
    live = 2
    oneUp_multiplier = 1
    playOneUpSFX = 0
    intensity = 0
    player = Player(display_width / 2, display_height / 2, gameDisplay, display_width, display_height, player_size)
    saucer = Saucer(display_width, display_height, gameDisplay)
    high_score = read_high_score()

    # Main loop
    while gameState != "Exit":
        handle_menu_music(gameState)    
        # Game menu
        while gameState == "Menu":
            update_scrolling_background()
            drawText("ASTEROIDS", white, display_width / 2, display_height / 2, 100)
            drawText("Press any key to START", white, display_width / 2, display_height / 2 + 100, 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    reset_high_score()  # Reset high score when closing the window
                    gameState = "Exit"
                if event.type == pygame.KEYDOWN:
                    gameState = "Playing"
                    # stop menu music
                    handle_menu_music(gameState)

            pygame.display.update()
            timer.tick(5)

        # highscore checker
        if score > high_score:
            high_score = score
            write_high_score(high_score)

        # User inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reset_high_score()  # Reset high score when exiting the game
                gameState = "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    if gameState == "Playing":
                        gameState = "Paused"
                    elif gameState == "Paused":
                        gameState = "Playing"
                    # start menu music
                    handle_menu_music(gameState)

                elif gameState == "Paused":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop("Playing")
                    elif event.key == pygame.K_q:
                        gameState = "Exit"
                        reset_high_score()  # Reset high score when exiting the game
                        pygame.quit()
                        quit()
                if event.key == pygame.K_UP:
                    player.thrust = True
                if event.key == pygame.K_LEFT:
                    player.rtspd = -player_max_rtspd
                if event.key == pygame.K_RIGHT:
                    player.rtspd = player_max_rtspd
                if event.key == pygame.K_SPACE and player_dying_delay == 0 and len(bullets) < bullet_capacity:
                    bullets.append(Bullet(player.x, player.y, player.dir, gameDisplay, display_width, display_height))
                    # Play SFX
                    pygame.mixer.Sound.play(snd_fire)
                if gameState == "Game Over":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop("Playing")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.thrust = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.rtspd = 0
            # Mousebutton clickable
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameState == "Paused" or gameState == "Game Over":
                    mouse_pos = pygame.mouse.get_pos()
                    buttons = draw_pause_menu(score) if gameState == "Paused" else draw_game_over_menu(score, high_score)
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            action = handle_button_click(button["text"], score)
                            if action == "Playing":
                                gameState = "Playing"
                            elif action == "Restart":
                                gameState = "Exit"
                                gameLoop("Playing")
                            elif action == "Exit":
                                gameState = "Exit"
                                pygame.quit()
                                quit()

        # Update player
        player.updatePlayer()

        # Checking player invincible time
        if player_invi_dur != 0:
            player_invi_dur -= 1

        # Reset display
        gameDisplay.fill(black)

        # Draw pause menu if game is paused
        if gameState == "Paused":
            draw_pause_menu(score)
            pygame.display.update()
            timer.tick(5)
            continue  # Skip the rest of the loop

        # If game is over, display game over menu with real highscore
        elif gameState == "Game Over":
            update_scrolling_background()
            handle_menu_music(gameState)
            buttons = draw_game_over_menu(score, high_score)
            pygame.display.update()
            timer.tick(5)
            continue  # Skip the rest of the loop

        for power_up in powerups:
            power_up.draw(gameDisplay)
            if power_up.collides_with_player(player):  # Übergeben Sie das 'player'-Objekt
                if not power_up.is_activated:  # Überprüfen Sie, ob das Power-Up bereits aktiviert wurde
                    power_up.activate()  # Aktivieren Sie das Power-Up
                    active_powerups.append(power_up)  # Fügen Sie das Power-Up zur Liste der aktiven Power-Ups hinzu
                    print(active_powerups)
                    powerups.remove(power_up)  # Entfernen Sie das Power-Up aus der Liste
        for power_up in active_powerups.copy():  # Verwenden Sie .copy() um über eine Kopie der Liste zu iterieren
            power_up.update()  # Aktualisieren Sie den Zustand des Power-Ups

            # Überprüfen Sie, ob das Power-Up noch aktiv ist
            if not power_up.active:
                # Wenn das Power-Up nicht mehr aktiv ist, entfernen Sie es aus der Liste
                active_powerups.remove(power_up)
            elif isinstance(power_up, power_ups.Shield):
                # Wenn das Schild aktiv ist, zeichnen Sie eine  Umrandung um den Spieler
                pygame.draw.circle(gameDisplay, (173, 216, 250), (int(player.x), int(player.y)), player_size + 10, 2)

        
        # Check for collision w/ asteroid
        for a in asteroids:
            a.updateAsteroid()
            if player_state != "Died":
                if isColliding(player.x, player.y, a.x, a.y, a.size):
                    # Create ship fragments
                    player_pieces.append(DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                    player_pieces.append(DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                    player_pieces.append(DeadPlayer(player.x, player.y, player_size, gameDisplay))

                    # Kill player
                    player_state = "Died"
                    player_dying_delay = 30
                    player_invi_dur = 120
                    player.killPlayer()

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

        # Update ship fragments
        for f in player_pieces:
            f.updateDeadPlayer()
            if f.x > display_width or f.x < 0 or f.y > display_height or f.y < 0:
                player_pieces.remove(f)

        # Check for end of stage
        if len(asteroids) == 0 and saucer.state == "Dead":
            if next_level_delay < 30:
                next_level_delay += 1
            else:
                stage += 1
                intensity = 0
                # Spawn asteroid away of center
                for i in range(stage):
                    xTo = display_width / 2
                    yTo = display_height / 2
                    while xTo - display_width / 2 < display_width / 4 and yTo - display_height / 2 < display_height / 4:
                        xTo = random.randrange(0, display_width)
                        yTo = random.randrange(0, display_height)
                    asteroids.append(Asteroid(xTo, yTo, "Large", gameDisplay, display_width, display_height))
                next_level_delay = 0

        # Update intensity
        if intensity < stage * 450:
            intensity += 1

        # Saucer
        if saucer.state == "Dead":
            if random.randint(0, 6000) <= (intensity * 2) / (stage * 9) and next_level_delay == 0:
                saucer.createSaucer()
                # Only small saucers >40000
                if score >= 40000:
                    saucer.type = "Small"
        else:
            # Set saucer targer dir
            acc = small_saucer_accuracy * 4 / stage
            saucer.bdir = math.degrees(math.atan2(-saucer.y + player.y, -saucer.x + player.x) + math.radians(random.uniform(acc, -acc)))

            saucer.updateSaucer()
            saucer.drawSaucer()

            # Check for collision w/ asteroid
            for a in asteroids:
                if isColliding(saucer.x, saucer.y, a.x, a.y, a.size + saucer.size):
                    # Set saucer state
                    saucer.state = "Dead"

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
                        pygame.mixer.Sound.play(snd_bangM)
                    else:
                        # Play SFX
                        pygame.mixer.Sound.play(snd_bangS)
                    asteroids.remove(a)

            # Check for collision w/ bullet
            for b in bullets:
                if isColliding(b.x, b.y, saucer.x, saucer.y, saucer.size):
                    # Add points
                    if saucer.type == "Large":
                        score += 200
                        
                    else:
                        score += 1000

                    # Set saucer state
                    saucer.state = "Dead"
                    
                    # Wählen Sie zufällig ein Power-Up aus
                    power_up_type = random.choice(['Shield'])  # Wählen Sie zufällig ein Power-Up aus

                    if power_up_type == 'Shield':
                        new_power_up = power_ups.Shield(saucer.x, saucer.y, 'Assets/Powerups/Shield.png')
                        powerups.append(new_power_up)

                    # Play SFX
                    pygame.mixer.Sound.play(snd_bangL)

                    # Remove bullet
                    bullets.remove(b)

            # Check collision w/ player
            if isColliding(saucer.x, saucer.y, player.x, player.y, saucer.size):
                if player_state != "Died":
                    # Create ship fragments
                    player_pieces.append(DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                    player_pieces.append(DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                    player_pieces.append(DeadPlayer(player.x, player.y, player_size, gameDisplay))

                    # Kill player
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

            # Saucer's bullets
            for b in saucer.bullets:
                # Update bullets
                b.updateBullet()

                # Check for collision w/ asteroids
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

                        # Remove asteroid and bullet
                        asteroids.remove(a)
                        saucer.bullets.remove(b)

                        break

                # Check for collision w/ player
                if isColliding(player.x, player.y, b.x, b.y, 5):
                    if player_state != "Died":
                        # Create ship fragments
                        player_pieces.append(DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                        player_pieces.append(DeadPlayer(player.x, player.y, 5 * player_size / (2 * math.cos(math.atan(1 / 3))), gameDisplay))
                        player_pieces.append(DeadPlayer(player.x, player.y, player_size, gameDisplay))

                        # Kill player
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

                        # Remove bullet
                        saucer.bullets.remove(b)

                if b.life <= 0:
                    try:
                        saucer.bullets.remove(b)
                    except ValueError:
                        continue

        # Bullets
        for b in bullets:
            # Update bullets
            b.updateBullet()

            # Check for bullets collide w/ asteroid
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
                    bullets.remove(b)

                    break

            # Destroying bullets
            if b.life <= 0:
                try:
                    bullets.remove(b)
                except ValueError:
                    continue

        # Extra live
        if score > oneUp_multiplier * 10000:
            oneUp_multiplier += 1
            live += 1
            playOneUpSFX = 60
        # Play sfx
        if playOneUpSFX > 0:
            playOneUpSFX -= 1
            pygame.mixer.Sound.play(snd_extra, 60)

        # Draw player
        if gameState != "Game Over":
            if player_state == "Died":
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

        # Draw score and high score
        drawText(f"Score: {score}", white, 60, 20, 40, False)
        drawText(f"High Score: {high_score}", white, display_width - 350, 20, 40, False)
       
        # Draw Lives
        for l in range(live + 1):
            Player(75 + l * 25, 75, gameDisplay, display_width, display_height, player_size).drawPlayer()

        # Update screen
        pygame.display.update()

        # Tick fps
        clock.tick(30)


# Start game
gameLoop("Menu")

# End game
reset_high_score()  # Reset high score when the script ends
pygame.quit()
quit()