import pygame
import random

def crear_powerup(ANCHO_PANTALLA, ALTO_PANTALLA):
    ancho = 30
    alto = 30
    x = random.randint(ANCHO_PANTALLA, ANCHO_PANTALLA + 200)
    y = random.randint(0, ALTO_PANTALLA - alto)

    return {
        'rect': pygame.Rect(x, y, ancho, alto),
        'tipo': random.choice(['vida', 'velocidad']),
        'activo': True,
        'velocidad': -2
    }

def mover_powerups(powerups):
    for p in powerups:
        p['rect'].x += p['velocidad']

def dibujar_powerups(pantalla, powerups, imagenes):
    for p in powerups:
        if p['activo']:
            pantalla.blit(imagenes[p['tipo']], p['rect'])

def recoger_powerups(player, powerups, VIDAS_MAXIMAS):
    for p in powerups:
        if p['activo'] and player['rect'].colliderect(p['rect']):
            if p['tipo'] == 'vida':
                if player['vidas'] < VIDAS_MAXIMAS:
                    player['vidas'] += 1
            elif p['tipo'] == 'velocidad':
                player['velocidad'] += 1
            p['activo'] = False
