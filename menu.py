import pygame
from utils.button import create_button, draw_button, is_button_clicked
from utils.text import draw_text

# --- Menú Principal ---
def main_menu(screen: pygame.Surface, width: int, height: int, font_title: pygame.font.Font, button_font: pygame.font.Font, text_color: tuple, button_color: tuple, button_hover: tuple) -> str:
    """
    Muestra el menú principal y maneja la interacción con los botones.
    Retorna la acción seleccionada ('jugar', 'ranking', 'creditos', 'salir').
    """
    title_img = pygame.image.load("assets\\image\\title.png").convert_alpha()
    title_img = pygame.transform.scale(title_img, (400, 100))

    background_img = pygame.image.load("assets\\image\\background.jpg").convert()
    background_img = pygame.transform.scale(background_img, (width, height))

    icon_img = pygame.image.load("assets\\image\\weapon.png").convert_alpha()
    icon_img = pygame.transform.scale(icon_img, (30, 30))

    sound_click = pygame.mixer.Sound("assets\\sounds\\shoot.mp3")
    sound_hover = pygame.mixer.Sound("assets\\sounds\\selection.mp3")
    sound_click.set_volume(0.1)   # 50% del volumen
    sound_hover.set_volume(0.1)   # 50% del volumen
    buttons_hover_prev = set()

    # Lista de diccionarios de botones
    buttons = [
        create_button(width // 2 - 100, height // 2 - 80, 200, 60, "Jugar", "jugar"),
        create_button(width // 2 - 100, height // 2, 200, 60, "Ranking", "ranking"),
        create_button(width // 2 - 100, height // 2 + 80, 200, 60, "Créditos", "creditos"),
        create_button(width // 2 - 100, height // 2 + 160, 200, 60, "Salir", "salir")
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos() # Obtener la posición actual del mouse

        for button in buttons:
            if button['rect'].collidepoint(mouse_pos):
                if button['texto'] not in buttons_hover_prev:
                    if sound_hover:
                        sound_hover.play()
                    buttons_hover_prev.add(button['texto'])
            else:
                buttons_hover_prev.discard(button['texto'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir" # Si el usuario cierra la ventana, salir del juego
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Click izquierdo del mouse
                    for button in buttons:
                        if is_button_clicked(button, mouse_pos):
                            if sound_click:
                                sound_click.play()
                            pygame.time.delay(1000)  # Espera breve para oír el sound
                            return button['action'] # Retornar la acción del botón seleccionado

        screen.blit(background_img, (0, 0))

        title_rect = title_img.get_rect(center=(width // 2, int(height * 0.20)))
        screen.blit(title_img, title_rect)

        # Dibujar todos los botones
        for button in buttons:
            draw_button(screen, button, mouse_pos, button_color, button_hover, button_font, text_color, icon_img)

        pygame.display.flip() # Actualizar la pantalla
    
    return "salir"