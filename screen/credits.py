import pygame

from utils.image import load_image
from utils.soundtrack import play_music, stop_music
from utils.text import draw_text

def show_credits(screen: pygame.Surface, screen_size: dict, font_size: dict, colors: dict):

    play_music("credits_music.mp3", 0.05)

    background_image = load_image("credits_background.jpg", screen_size["width"], screen_size["height"], colors["black"])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False

        screen.blit(background_image, (0, 0))

        draw_text(screen, "Créditos", screen_size["width"] // 2, screen_size["height"] // 2 - 200, font_size["large"], colors["orange"], "center")
        
        draw_text(screen, "Este juego fue realizado para la materia Programación 1,", screen_size["width"] // 2, screen_size["height"] // 2 - 120, font_size["small"] - 6, colors["white"], "center")
        draw_text(screen, "división 316-1 de la Universidad Tecnológica Nacional", screen_size["width"] // 2, screen_size["height"] // 2 - 80, font_size["small"] - 6, colors["white"], "center")
        draw_text(screen, "Nombre del equipo: Cielo Letal", screen_size["width"] // 2, screen_size["height"] // 2 - 10, font_size["small"] - 6, colors["white"], "center")
        
        draw_text(screen, "Integrantes", screen_size["width"] // 2, screen_size["height"] // 2 + 40, font_size["small"] - 6, colors["orange"], "center")
        draw_text(screen, "Ezequiel Martín Quispe", screen_size["width"] // 2, screen_size["height"] // 2 + 80, font_size["small"] - 6, colors["white"], "center")
        draw_text(screen, "Federico Ezequiel Piretro Berengo", screen_size["width"] // 2, screen_size["height"] // 2 + 120, font_size["small"] - 6, colors["white"], "center")
        draw_text(screen, "Miqueas Servettini", screen_size["width"] // 2, screen_size["height"] // 2 + 160, font_size["small"] - 6, colors["white"], "center")

        draw_text(screen, "Presiona ESC o ENTER para volver", screen_size["width"] // 2, screen_size["height"] - 50, font_size["small"] - 12, colors["white"], "center")
        
        pygame.display.flip()

    stop_music()