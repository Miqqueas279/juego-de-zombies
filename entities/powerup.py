import random

import pygame

def create_powerup(screen_width: int, scree_height: int) -> dict:

    """
    Crea un power-up con posición y tipo aleatorios.
    """
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

def move_powerups(powerups:list[dict]) -> None:
    """
    Mueve los power-ups hacia la izquierda según su velocidad.

    """
    for p in powerups:
        p['rect'].x += p['velocidad']

def draw_powerups(screen: pygame.Surface, powerups: list[dict], image: dict[str, pygame.Surface]) -> None:
    """
    Dibuja los power-ups activos en la pantalla.

    """
    for p in powerups:
        if p['activo']:
            screen.blit(image[p['tipo']], p['rect'])

def pick_up_powerup(player: dict, powerups: list[dict], max_health: int) -> None:
    """
    Verifica colisiones entre el jugador y power-ups, aplica efectos y desactiva los recogidos.
    """

    for p in powerups:
        if p['activo'] and player['rect'].colliderect(p['rect']):
            if p['tipo'] == 'vida':
                if player['vidas'] < max_health:
                    player['vidas'] += 1
            elif p['tipo'] == 'velocidad':
                player['velocidad'] += 1
            p['activo'] = False
