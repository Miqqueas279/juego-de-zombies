import pygame

def detectar_colision_rect(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    Detecta si dos objetos pygame.Rect están colisionando.
    """
    return rect1.colliderect(rect2)
