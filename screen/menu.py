import pygame

from utils.button import create_button, draw_button, is_button_clicked
from utils.image import load_image
from utils.soundtrack import load_sound, play_music
from utils.story import show_intro_story  # <-- IMPORTAR LA HISTORIA

# --- Menú Principal ---
def main_menu(screen: pygame.Surface, screen_size: dict, font_size: dict, colors: dict) -> str:
    """
    Muestra el menú principal y maneja la interacción con los botones.
    Retorna la acción seleccionada ('jugar', 'ranking', 'creditos', 'salir').
    """
    play_music("menu_music.ogg", 0.05)

    title_image = load_image("title.png", 400, 100, colors["white"])
    background_image = load_image("background.jpg", screen_size["width"], screen_size["height"], colors["black"])
    icon_image = load_image("weapon.png", 30, 30, colors["white"])

    sound_click = load_sound("shoot.mp3", 0.1)
    sound_hover = load_sound("selection.mp3", 0.1)
    buttons_hover_prev = set()

    # Lista de botones
    buttons = [
        create_button(screen_size["width"] // 2 - 100, screen_size["height"] // 2 - 80, 200, 60, "Jugar", "jugar"),
        create_button(screen_size["width"] // 2 - 100, screen_size["height"] // 2, 200, 60, "Ranking", "ranking"),
        create_button(screen_size["width"] // 2 - 100, screen_size["height"] // 2 + 80, 200, 60, "Créditos", "creditos"),
        create_button(screen_size["width"] // 2 - 100, screen_size["height"] // 2 + 160, 200, 60, "Salir", "salir")
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

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
                return "salir"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        if is_button_clicked(button, mouse_pos):
                            if sound_click:
                                sound_click.play()
                            pygame.time.delay(500)

                            if button['action'] == "jugar":
                                show_intro_story(screen, screen_size["width"], screen_size["height"], font_size["small"], colors)  # 🎬 Mostrar historia

                            return button['action']

        screen.blit(background_image, (0, 0))

        title_rect = title_image.get_rect(center=(screen_size["width"] // 2, int(screen_size["height"] * 0.20)))
        screen.blit(title_image, title_rect)

        for button in buttons:
            draw_button(screen, button, mouse_pos, colors["white"], colors["orange"], font_size["small"], icon_image)

        pygame.display.flip()

    return "salir"
