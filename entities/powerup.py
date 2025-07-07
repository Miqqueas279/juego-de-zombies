import random

import pygame

def create_powerup(screen_width: int, scree_height: int) -> dict:

    """
    Crea un power-up con posición y tipo aleatorios.

    Args:
        screen_width (int): Ancho de la pantalla.
        screen_height (int): Alto de la pantalla.

    Returns:
        dict: Diccionario con las propiedades del power-up.
              Contiene:
              - 'rect': pygame.Rect con posición y tamaño.
              - 'tipo': str ('vida' o 'velocidad').
              - 'activo': bool, si está activo.
              - 'velocidad': int, velocidad de desplazamiento (negativa hacia la izquierda).
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

    Args:
        powerups (list[dict]): Lista de diccionarios que representan power-ups.
    """
    for p in powerups:
        p['rect'].x += p['velocidad']

def draw_powerups(screen: pygame.Surface, powerups: list[dict], image: dict[str, pygame.Surface]) -> None:
    """
    Dibuja los power-ups activos en la pantalla.

    Args:
        screen (pygame.Surface): Superficie donde se dibujan los power-ups.
        powerups (list[dict]): Lista de power-ups.
        image (dict[str, pygame.Surface]): Diccionario con imágenes para cada tipo de power-up.
    """
    for p in powerups:
        if p['activo']:
            screen.blit(image[p['tipo']], p['rect'])

def pick_up_powerup(player: dict, powerups: list[dict], max_health: int) -> None:
    """
    Verifica colisiones entre el jugador y power-ups, aplica efectos y desactiva los recogidos.

    Args:
        player (dict): Diccionario con información del jugador. Espera claves 'rect', 'vidas', 'velocidad'.
        powerups (list[dict]): Lista de power-ups.
        max_health (int): Cantidad máxima de vidas permitidas para el jugador.
    """

    for p in powerups:
        if p['activo'] and player['rect'].colliderect(p['rect']):
            if p['tipo'] == 'vida':
                if player['vidas'] < max_health:
                    player['vidas'] += 1
            elif p['tipo'] == 'velocidad':
                player['velocidad'] += 1
            p['activo'] = False
