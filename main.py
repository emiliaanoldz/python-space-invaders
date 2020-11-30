import math
import random

import pygame
from pygame import mixer

# Iniciar pygame
pygame.init()

# Crear ventana
screen = pygame.display.set_mode((800, 600))

# Fondo
background = pygame.image.load('background.png')

# Sonido de fondo
mixer.music.load("cancion.mp3")
mixer.music.play(-1)

# Titulo e icono
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Jugador
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Array de Enemigos
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bala
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
isReady = True

# Puntaje
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
# Posicion puntaje
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Puntaje: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def pause():
    mixer.music.load("pausa.mp3")
    mixer.music.play(1)
    paused = True
    while paused:
        paused_text = over_font.render("PAUSA", True, (255, 255, 255))
        screen.blit(paused_text, (300, 400))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        pygame.display.update()

    mixer.music.load("cancion.mp3")
    mixer.music.play(-1)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global isReady
    isReady = False
    screen.blit(bulletImg, (x + 16, y + 10))
    # 16 y 10 para centrar la bala y que salga desde la punta de la nave.


# Calcular distancia entre dos coordenadas http://www.profesorenlinea.cl/imagengeometria/Distancia_entre_dos_puntos_image001.gif
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    # Imagen de Fondo
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Eventos de teclas presionadas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause()
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if isReady:
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Seteamos bulletX con la posicion de la nave.
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # Limites para no salirse de la pantalla.
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Creacion y movimiento de los enemigos
    for i in range(num_of_enemies):

        # Game Over si el enemigo llega a 441 en eje Y
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # Si va a la izquierda, le cambiamos la dirección
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        # Si va a la derecha, le cambiamos la dirección
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.mp3")
            explosionSound.play()
            # Bala en 0 para resetear su eje Y
            bulletY = 0
            isReady = True
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # Creamos al enemigo con los datos generados y lo pintamos en pantalla.
        enemy(enemyX[i], enemyY[i], i)

    # Movimiento de Bala, si es menor a 0 en el eje Y, la seteamos como isReady.
    if bulletY <= 0:
        bulletY = 480
        isReady = True
    # Mientras la bala sea isReady=False, le vamos restando el valor bulletY_change para ir moviendola.
    if isReady is False:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
