import pygame
import random
import math


# Inicializar pygame
pygame.init()

#Para crear la pantalla
pantalla = pygame.display.set_mode((800,600))

#Titulo e icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load('ovni.png')
pygame.display.set_icon(icono)

#Fondo
fondo = pygame.image.load('Fondo.jpg')

#Puntaje del juego
puntaje = 0

#Variables del Jugador
jugador_img = pygame.image.load('cohete.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0


#Variables del enemigo
enemigo_img = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 5


for e in range(cantidad_enemigos):
    enemigo_img.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

#Variables de la bala
bala_img = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

#Funcion jugador
def jugador(x,y):
    pantalla.blit(jugador_img,(x,y))

#Funcion del enemigo
def enemigo(x,y,ene):
    pantalla.blit(enemigo_img[ene],(x,y))

#Funcion de la bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    #Se le agrega 16, y 10 a x y y respectivamente para que la bala empiece desde el medio de la nave
    pantalla.blit(bala_img,(x+16,y+10))

#Funcion para detectar colisiones
def existe_colision(x_1,x_2,y_1,y_2):
    distancia = math.sqrt((math.pow(x_1-x_2 ,2)) + (math.pow(y_2 - y_1,2)))
    if distancia < 27:
        return True
    else:
        return False

se_ejecuta = True
##Loop del juego
while se_ejecuta:
    #RGB de la pantalla
    pantalla.blit(fondo,(0,0))
    #Eventos para controlar movimientos, etc
    for evento in pygame.event.get():
        #Evento que indica si el usuario dio click sobre el icono de cerrar ventana
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1

            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x,bala_y)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #Modificar la posision del jugador
    jugador_x += jugador_x_cambio
    #Mantenerl al jugador en el limite de las pantallas
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar la posision del enemigo
    for e in range(cantidad_enemigos):
        enemigo_x[e] += enemigo_y_cambio[e]

        # Mantenerl al jugador en el limite de las pantallas
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] +=enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1
            enemigo_y[e] += enemigo_y_cambio[e]

        # Para detectar colisiones
        colision = existe_colision(enemigo_x[e], bala_x, enemigo_y[e], bala_y)
        if colision:
            bala_y = 500
            bala_visible = False
            puntaje += 1
            print(puntaje)
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

    enemigo(enemigo_x[e], enemigo_y[e],e)

    #Movimiento de la bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio



    jugador(jugador_x,jugador_y)

    #Actualiza todos los recursos
    pygame.display.update()