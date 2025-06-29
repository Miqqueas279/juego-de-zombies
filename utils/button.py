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

def draw_button(screen: pygame.Surface, button: dict, mouse_pos: tuple, button_color: tuple, button_hover: tuple, button_font: pygame.font.Font, text_color: tuple, icon_img: pygame.Surface ) -> None:
    """
    Dibuja un botón en la pantalla, cambiando de color al pasar el mouse.
    """
    #pygame.draw.rect(screen, color, button['rect'], border_radius=10)

    # Posición para la imagen (alineada a la izquierda del botón)
    icon_x = button['rect'].x + 10
    icon_y = button['rect'].centery - icon_img.get_height() // 2

    # Posición para el texto (a la derecha de la imagen)
    text_x = icon_x + icon_img.get_width() + 15
    text_y = button['rect'].centery

    if button['rect'].collidepoint(mouse_pos):
        color = button_hover
        screen.blit(icon_img, (icon_x, icon_y))

    else:
        color = button_color

    draw_text(screen, button['texto'], text_x, text_y, button_font.get_height(), color, "left", font=button_font)

def is_button_clicked(button: dict, mouse_pos: tuple) -> bool:
    """
    Verifica si un botón ha sido seleccionado.
    """
    return button['rect'].collidepoint(mouse_pos)