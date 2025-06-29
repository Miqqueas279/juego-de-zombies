import pygame
import os

def get_font(size):
    """
    Obtiene una fuente por defecto de Pygame del tamaño especificado.
    Útil para asegurar que las fuentes estén disponibles.
    """
    ruta_fuente = os.path.join("assets", "fonts", "Zombies.otf")
    return pygame.font.Font(ruta_fuente, size)

def draw_text(pantalla, texto, x, y, tamano_fuente, color, align, font=None ):
    """
    Dibuja texto en la pantalla centrado en las coordenadas dadas.
    Si no se proporciona una fuente, usa una por defecto.
    """
    if font is None:
        fuente_obj = font
    else:
        fuente_obj = get_font(tamano_fuente) # Usar la función get_font

    shadow_surface = fuente_obj.render(texto, True, (0, 0, 0))
    superficie_texto = fuente_obj.render(texto, True, (255, 255, 255))

    if align == "left":
        shadow_rect = shadow_surface.get_rect(midleft=(x + 2, y + 2))
        rect_texto = superficie_texto.get_rect(midleft=(x, y))
    else: 
        shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
        rect_texto = superficie_texto.get_rect(center=(x, y))
    
    pantalla.blit(shadow_surface, shadow_rect)
    pantalla.blit(superficie_texto, rect_texto)