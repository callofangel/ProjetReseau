import sys
import pygame
import socket


###########
###############################################
HOST = "localhost"
PORT = 9000

# Initialisation du serveur
# Mise en place du socket avec les protocoles IPv4 et TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#################################################
#####################


# Screen setup

width = 800
height = 600

clay = (0xFF, 0x40, 0)

ball_speed = [ -2, -2 ]
racket_speed_droite = [0, 0]
racket_speed_gauche = [0, 0]
x2 = 0
la_balle = 0


# Pygame initialization
pygame.init()
screen = pygame.display.set_mode( (width, height) )


# Load resources
ball_load = pygame.image.load("./image/ball.png")
ball_coords = ball_load.get_rect()


racket_droite = pygame.image.load("./image/racket.png")
racket_coords_droite = racket_droite.get_rect()

racket_gauche = pygame.image.load("./image/racket.png")
racket_coords_gauche = racket_gauche.get_rect()

# Throw ball from center
def throw():
    ball_coords.left = 531
    ball_coords.top = 298

throw()

def ball_lost():
    # Racket reached racket position?
    if ball_coords.left <= 0:
        if ball_coords.bottom <= racket_coords_gauche.top or ball_coords.top >= racket_coords_gauche.bottom:
            print("lost!")
            throw()





while True:
    for e in pygame.event.get():
        # Check for exit
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                racket_speed_droite[1] = -4
                pass
            elif e.key == pygame.K_RIGHT:
                racket_speed_droite[1] = 4
                pass

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                racket_speed_droite[1] = 0
                pass
            elif e.key == pygame.K_RIGHT:
                racket_speed_droite[1] = 0
                pass


    # Bounce ball on walls
    if ball_coords.left < 0 or ball_coords.right >= width:
        ball_speed[0] = -ball_speed[0]
    if ball_coords.top < 0 or ball_coords.bottom >= height:
        ball_speed[1] = -ball_speed[1]

    # Move racket
    racket_coords_droite = racket_coords_droite.move(racket_speed_droite)
    racket_coords_gauche = racket_coords_gauche.move(racket_speed_gauche)


        # Clip racket on court
    if racket_coords_droite.left < 0:
        racket_coords_droite.left = 0
    elif racket_coords_droite.right >= width:
        racket_coords_droite.right = width - 1
    if racket_coords_droite.top < 0:
        racket_coords_droite.top = 0
    elif racket_coords_droite.bottom >= height:
        racket_coords_droite.bottom = height - 1

    if racket_coords_gauche.left < 0:
        racket_coords_gauche.left = 0
    elif racket_coords_gauche.right >= width:
        racket_coords_gauche.right = width - 1
    if racket_coords_gauche.top < 0:
        racket_coords_gauche.top = 0
    elif racket_coords_gauche.bottom >= height:
        racket_coords_gauche.bottom = height - 1

    if ball_coords.right >= 800:
        if ball_coords.bottom <= racket_coords_droite.top or ball_coords.top >= racket_coords_droite.bottom:
            print("lost!")
            throw()

    # affichage
    screen.fill(clay)
    screen.blit(racket_droite, racket_coords_droite)

#########################################################
#########################################################

    # reception racketgauche
    for i in range(2):
        recu = s.recv(1024).decode('utf-8')
        spliter =recu.split(":")
        # print(spliter)
        toutslesmot = spliter
        premierMot = toutslesmot[0]

        # reception ball
        if premierMot == "ball":
            x = int(toutslesmot[1])
            y = int(toutslesmot[2])

            ball_coords.x = x
            ball_coords.y = y

            screen.blit(ball_load, ball_coords)

        #########################################################
        #########################################################

        if premierMot == "coordonéeRocketgauche":
            raquettex = int(toutslesmot[1])
            raquettey = int(toutslesmot[2])

            racket_coords_gauche.x = raquettex
            racket_coords_gauche.y = raquettey
            screen.blit(racket_gauche, racket_coords_gauche)



#########################################################
#########################################################

        #Envoie de données de la rackette droite

        racketx = racket_coords_droite.x = 800
        rackety = racket_coords_droite.y
        a = "coordonéeRocketdroite" + ":" + str(racketx) + ":" + str(rackety) + ":"
        s.send(a.encode('utf-8'))

#########################################################
#########################################################

    pygame.display.flip()
    # sleep 10ms, since there is no need for more than 100Hz refresh :)
    pygame.time.delay(10)


socket.close()
