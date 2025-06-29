import pygame
from utils.text import draw_text

# --- Funciones para Botones ---

def create_button(x: int, y: int, width: int, height: int, texto: str, action: str) -> dict:
    """
    Crea un diccionario que representa los datos de un botón.
    """
    return {
        'rect': pygame.Rect(x, y, width, height),
        'texto': texto,
        'action': action
    }

def draw_button(screen: pygame.Surface, button: dict, mouse_pos: tuple, button_color: tuple, button_hover: tuple, button_font: pygame.font.Font, text_color: tuple) -> None:
    """
    Dibuja un botón en la pantalla, cambiando de color al pasar el mouse.
    """
    if button['rect'].collidepoint(mouse_pos):
        color = button_hover
    else:
        color = button_color
    
    pygame.draw.rect(screen, color, button['rect'], border_radius=10)
    draw_text(screen, button['texto'], button['rect'].centerx, button['rect'].centery, button_font.get_height(), text_color, font=button_font)

def is_button_clicked(button: dict, mouse_pos: tuple) -> bool:
    """
    Verifica si un botón ha sido seleccionado.
    """
    return button['rect'].collidepoint(mouse_pos)