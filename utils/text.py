import pygame
import os

# Definir BASE_DIR para que las rutas de fuentes funcionen correctamente
# BASE_DIR será la carpeta raíz del proyecto (juego-de-zombies)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Apunta a la carpeta 'JUEGO-DE-ZOMBIES'

def get_font(size):
    """
    Obtiene la fuente 'Zombies.otf' del tamaño especificado.
    Si la fuente no se encuentra, usa la fuente predeterminada de Pygame.
    """
    # Construir la ruta absoluta a la fuente desde la raíz del proyecto
    ruta_fuente = os.path.join(BASE_DIR, 'assets', 'fonts', 'Zombies.otf')
    
    # Carga directa de la fuente (sin try-except)
    return pygame.font.Font(ruta_fuente, size) # Se asume que la fuente existe y se carga correctamente

def draw_text(pantalla, texto, x, y, tamano_fuente, color, align, font=None ):
    """
    Dibuja texto en la pantalla con sombra y alineación.
    Si no se proporciona un objeto de fuente, usa get_font para obtener uno.
    """
    # Si se proporciona un objeto de fuente, úsalo. Si no, crea uno nuevo con get_font.
    fuente_obj = font if font is not None else get_font(tamano_fuente)

    # Renderizar el texto para la sombra (negro) y el texto principal (color deseado)
    shadow_surface = fuente_obj.render(texto, True, (0, 0, 0)) # Sombra negra
    superficie_texto = fuente_obj.render(texto, True, color) # Texto con el color deseado

    # Determinar la posición del rectángulo de texto según la alineación
    if align == "left":
        # Para alineación izquierda, midleft (centro vertical, borde izquierdo horizontal)
        shadow_rect = shadow_surface.get_rect(midleft=(x + 2, y + 2))
        rect_texto = superficie_texto.get_rect(midleft=(x, y))
    elif align == "right":
        # Para alineación derecha, midright (centro vertical, borde derecho horizontal)
        shadow_rect = shadow_surface.get_rect(midright=(x - 2, y + 2)) # Sombra desplazada
        rect_texto = superficie_texto.get_rect(midright=(x, y))
    else: # align == "center" o cualquier otro valor por defecto
        # Para alineación central (por defecto), center (centro horizontal y vertical)
        shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2)) # Sombra desplazada
        rect_texto = superficie_texto.get_rect(center=(x, y))
    
    # Dibujar la sombra y luego el texto principal para el efecto de profundidad
    pantalla.blit(shadow_surface, shadow_rect)
    pantalla.blit(superficie_texto, rect_texto)
