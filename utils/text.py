import pygame
import os

def get_font(size):
    """
    Obtiene una fuente por defecto de Pygame del tamaño especificado.
    Útil para asegurar que las fuentes estén disponibles.
    """
    ruta_fuente = os.path.join("assets", "fonts", "Zombies.otf")
    return pygame.font.Font(ruta_fuente, size)

def draw_text(pantalla, texto, x, y, tamano_fuente, color, font=None):
    """
    Dibuja texto en la pantalla centrado en las coordenadas dadas.
    Si no se proporciona una fuente, usa una por defecto.
    """
    if font is None:
        fuente_obj = font
    else:
        fuente_obj = get_font(tamano_fuente) # Usar la función get_font


    superficie_texto = fuente_obj.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y))
    pantalla.blit(superficie_texto, rect_texto)