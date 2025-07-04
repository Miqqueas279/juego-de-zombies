import pygame
from utils.button import create_button, draw_button, is_button_clicked
from utils.image import load_image
from utils.soundtrack import load_sound, play_music

# --- Menú Principal ---
def main_menu(screen: pygame.Surface, width: int, height: int, button_font: pygame.font.Font, colors: dict) -> str:
    """
    Muestra el menú principal y maneja la interacción con los botones.
    Retorna la acción seleccionada ('jugar', 'ranking', 'creditos', 'salir').
    """
    play_music("menu_music.ogg", 0.05)

    title_image = load_image("title.png", 400, 100, colors["white"])
    background_image = load_image("background.jpg", width, height, colors["black"])
    icon_image = load_image("weapon.png", 30, 30, colors["white"])

    sound_click = load_sound("shoot.mp3", 0.1)
    sound_hover = load_sound("selection.mp3", 0.1)
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
                            pygame.time.delay(500)  # Espera breve para oír el sound
                            return button['action'] # Retornar la acción del botón seleccionado

        screen.blit(background_image, (0, 0))

        title_rect = title_image.get_rect(center=(width // 2, int(height * 0.20)))
        screen.blit(title_image, title_rect)

        # Dibujar todos los botones
        for button in buttons:
            draw_button(screen, button, mouse_pos, colors["white"], colors["orange"], button_font, icon_image)

        pygame.display.flip() # Actualizar la pantalla
    
    return "salir"