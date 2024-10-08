# Spaceroids

## Beschreibung
Asteroids ist ein klassisches Arcade-Spiel, bei dem der Spieler ein Raumschiff steuert und Asteroiden zerstören muss, um Punkte zu sammeln. Das Ziel des Spiels ist es, so viele Punkte wie möglich zu erzielen, indem man Asteroiden ausweicht und sie abschießt. **Spaceroids** ist unsere Version des Spielklassikers mit einigen zusätzlichen Features wie Powerups, Design-Implementationen und mehr.

## Installation

### Voraussetzungen

- Python 3.x
- Pygame
- PyCharm (IDE)

### Installationsanweisung

1. Installieren Sie Python und Pygame auf Ihrem Computer.
2. Installieren Sie PyCharm als Entwicklungsumgebung, falls es nicht vorhanden ist.
3. Öffnen Sie PyCharm und wählen Sie **Open** aus dem **File-Menü*. Navigieren Sie zum Verzeichnis, in das Sie das Repository gepeichert haben, und wählen Sie es aus.
4. Stellen Sie sicher, dass die erforderlichen Bibliotheken installiert sind. Öffnen Sie das Terminal in PyCharm und führen Sie den folgenden Befehl aus: `pip install -r requirements.txt`
5. Öffnen Sie die Datei `main.py` in PyCharm.
6. Führen Sie das Spiel aus, indem Sie auf das grüne Dreieck (Run-Button) oben rechts klicken oder `Shift + F10` drücken.

## Handysteuerung

### Handy: Android App
Installieren Sie die bereitgestellte App und öffnen Sie diese.
Und stellen Sie sicher, dass das Handy und Laptop mit einem nicht-eingeschränkten Netzwerk (nicht Uni-Wlan) verbunden sind.

### Aktivierung der Handysteuerung

1. Installieren Sie die bereitgestellte App auf Ihrem Handy.
2. Öffnen Sie die App. Die App verbindet sich mittels des TCP-Protokolls und einer Socket-Server-Client-Kommunikation mit dem Spiel und sendet je nach Aktion ein entsprechendes Signal an das Spiel, um den Spieler zu steuern.
3. Sobald eine Verbindung zur App hergestellt wurde, kann man auf der App das Spiel ebenfalls direkt starten.
4. Durch die Verbindung lässt sich das Raumschiff auf dem Bildschirm Ihres Laptops oder anderen digitalen Endgeräten steuern. Dafür ist ein Steuerkreuz dargestellt, um zu schießen, steht Ihnen ein weiterer Button zur Verfügung.

## Spielanleitung

### Steuerung

- **Pfeiltasten**: Bewege das Raumschiff
- **Leertaste**: Schieße

### Handysteuerung
- **Steuerkreuz**: Bewege das Raumschiff
- **Button**: Schießen



### Ziel des Spiels
Zerstöre so viele Asteroiden wie möglich,
ohne von ihnen getroffen zu werden. Sammle Punkte, um den Highscore zu schlagen. Und Teile diesen Mit deinen Freunden.

## Features

- Klassisches Arcade-Gameplay
- Zufällig generierte Asteroiden je nach Schwierigkeitsgrad
- Highscore-System 
- Verschiedene Schwierigkeitsstufen
- Powerups und Design-Implementationen
- Handysteuerung





## Credits


- **Entwickler**: Marcel Seibt, Konrad Kindermann, Karan Soni.
- **Verwendete Bibliotheken**: Pygame


- Code Quellen:
Chat GPT,
Claude 3.5 Sonnet,
Github Copilot

- verwendetes Github Repository: 
Hung Le aka “ixora-0” (GitHub Username) (2018), GitHub,
	https://github.com/ixora-0/Asteroids

Grafiken:

- Menü Hintergrundbild vom User “ahasanaraakter” (2018), Vecteezy, https://www.vecteezy.com/photo/24448956-space-wallpaper-banner-background-stunning-view-of-a-cosmic-galaxy-with-planets-and-space-objects-elements-of-this-image-furnished-by-nasa-generate-ai
- Fliegende Untertasse Sprite vom User “Pixelgedon” (2018, 11. Januar), Deviantart,
	https://www.deviantart.com/pixelgedon/art/8Bit-Flying-Saucer-725060741
- Brown Asteroid Sprite vom User “FunwithPixels” (2017, 20. November), OpenGameArt,
	https://opengameart.org/content/brown-asteroid
- Tiny Spaceship Sprite vom User “Fearless Design” (Herausgabe, Unbekannt), itch.io,
	https://fearless-design.itch.io/tiny-ships-free-spaceships

Sounds:

- Menümusik:vom User “lowenergygirl” (2022), Soundcloud, https://soundcloud.com/lowenergygirl/1-into-the-spaceship oder https://lowenergygirl.itch.io/space-journey 
- Powerup Sounds: 
          https://sfxr.me/
