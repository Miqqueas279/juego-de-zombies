import os

import pygame

def get_font(size: int):
    """
    Obtiene una fuente por defecto de Pygame del tamaño especificado.
    Útil para asegurar que las fuentes estén disponibles.
    """
    font_path = os.path.join("assets", "fonts", "Zombies.otf")
    return pygame.font.Font(font_path, size)

def draw_text(screen: pygame.Surface, text: str, x: int, y: int, font_size: int, color: tuple, align: str ):
    """
    Dibuja texto en la pantalla centrado en las coordenadas dadas.
    Si no se proporciona una fuente, usa una por defecto.
    """
    font = get_font(font_size)

    shadow_surface = font.render(text, True, (0, 0, 0))
    text_surface = font.render(text, True, color)

    if align == "left":
        shadow_rect = shadow_surface.get_rect(midleft=(x + 2, y + 2))
        rect_texto = text_surface.get_rect(midleft=(x, y))
    else: 
        shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
        rect_texto = text_surface.get_rect(center=(x, y))
    
    screen.blit(shadow_surface, shadow_rect)
    screen.blit(text_surface, rect_texto)