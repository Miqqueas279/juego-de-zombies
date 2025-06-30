import pygame
import random

VELOCIDAD_ENEMIGO_BASE = 2
# Probabilidades de tipos de enemigos
PROBABILIDAD_BOOSTED = 0.2 # 20% de probabilidad de enemigo con boost
PROBABILIDAD_KAMIKAZE = 0.1 # 10% de probabilidad de kamikaze
# Multiplicadores de velocidad para enemigos especiales
FACTOR_VELOCIDAD_BOOSTED = 1.5 # Los enemigos con boost son 50% más rápidos
FACTOR_VELOCIDAD_KAMIKAZE = 3.0 # Los kamikazes son 200% más rápidos
VIDA_KAMIKAZE = 1 # Los kamikazes tienen poca vida
# Puntos que otorgan los enemigos
PUNTAJE_NORMAL = 10
PUNTAJE_BOOSTED = 15
PUNTAJE_KAMIKAZE = 25

def generar_enemigo(ANCHO_PANTALLA):
    """
    Crea un nuevo diccionario de enemigo con propiedades aleatorias.
    """
    enemy_ancho = 40
    enemy_alto = 40
    # Posición X aleatoria en la parte superior
    x_pos = random.randint(enemy_ancho // 2, ANCHO_PANTALLA - enemy_ancho // 2)
    y_pos = -enemy_alto # Empieza justo fuera de la pantalla por arriba

    # Propiedades base
    velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE
    vida_enemigo = 1
    puntaje_enemigo = PUNTAJE_NORMAL
    tipo_enemigo = "normal"

    # Determinar tipo de enemigo especial
    r = random.random()
    if r < PROBABILIDAD_KAMIKAZE:
        tipo_enemigo = "kamikaze"
        velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE * FACTOR_VELOCIDAD_KAMIKAZE
        vida_enemigo = VIDA_KAMIKAZE
        puntaje_enemigo = PUNTAJE_KAMIKAZE
    elif r < PROBABILIDAD_KAMIKAZE + PROBABILIDAD_BOOSTED: # Suma las probabilidades para que no se solapen
        tipo_enemigo = "boosted"
        velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE * FACTOR_VELOCIDAD_BOOSTED
        puntaje_enemigo = PUNTAJE_BOOSTED
    
    return {
        'rect': pygame.Rect(x_pos - enemy_ancho // 2, y_pos - enemy_alto // 2, enemy_ancho, enemy_alto),
        'velocidad': velocidad_enemigo,
        'vida': vida_enemigo,
        'tipo': tipo_enemigo,
        'puntos': puntaje_enemigo # Puntos que otorga al ser destruido
    }

def mover_enemigos(enemigos_list):
    """
    Actualiza la posición de todos los enemigos en la lista.
    """
    for enemigo in enemigos_list:
        enemigo['rect'].y += enemigo['velocidad']

def dibujar_enemigos(pantalla, enemigos_list, enemy_image):
    """
    Dibuja todos los enemigos en la pantalla.
    """
    for enemigo in enemigos_list:
        pantalla.blit(enemy_image, enemigo['rect'])