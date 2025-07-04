import pygame
import random

def create_powerup(screen_width, scree_height):
    width = 30
    height = 30
    x = random.randint(screen_width, scree_height + 200)
    y = random.randint(0, scree_height - width)

    return {
        'rect': pygame.Rect(x, y, width, height),
        'tipo': random.choice(['vida', 'velocidad']),
        'activo': True,
        'velocidad': -2
    }

def move_powerups(powerups):
    for p in powerups:
        p['rect'].x += p['velocidad']

def draw_powerups(screen, powerups, image):
    for p in powerups:
        if p['activo']:
            screen.blit(image[p['tipo']], p['rect'])

def pick_up_powerup(player, powerups, max_health):
    for p in powerups:
        if p['activo'] and player['rect'].colliderect(p['rect']):
            if p['tipo'] == 'vida':
                if player['vidas'] < max_health:
                    player['vidas'] += 1
            elif p['tipo'] == 'velocidad':
                player['velocidad'] += 1
            p['activo'] = False
