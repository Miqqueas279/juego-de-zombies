import pygame
from utils.text import draw_text # Asegurarse de que draw_text esté disponible

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

def draw_button(screen: pygame.Surface, button: dict, mouse_pos: tuple, button_color: tuple, button_hover: tuple, button_font: pygame.font.Font, text_color: tuple, border_color: tuple = (0, 0, 0)) -> None:
    """
    Dibuja un botón en la pantalla, cambiando de color al pasar el mouse.
    Recibe un color para el borde.
    """
    current_color = button_color
    if button['rect'].collidepoint(mouse_pos):
        current_color = button_hover
    
    # Dibujar el rectángulo del botón
    pygame.draw.rect(screen, current_color, button['rect'], border_radius=10)
    
    # Dibujar el borde del botón
    pygame.draw.rect(screen, border_color, button['rect'], 3, border_radius=10) # Borde de 3 píxeles de grosor

    # Dibujar el texto del botón
    # draw_text ahora requiere el parámetro 'align'
    draw_text(screen, button['texto'], button['rect'].centerx, button['rect'].centery, 
            button_font.get_height(), text_color, "center", font=button_font)

def is_button_clicked(button: dict, mouse_pos: tuple) -> bool:
    """
    Verifica si un botón ha sido seleccionado.
    """
    return button['rect'].collidepoint(mouse_pos)
