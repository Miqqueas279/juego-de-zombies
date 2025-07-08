import pygame

from utils.image import load_image
from utils.list import sort_list
from utils.text import draw_text

def show_ranking(screen: pygame.Surface, screen_size: dict, font_size: dict, colors: dict, scores: list[dict]) -> None:
    """
    Muestra la pantalla de ranking con los mejores puntajes del juego.
    """
    width = screen_size["width"]
    height = screen_size["height"]

    background_image = load_image("background.jpg", width, height, colors["black"])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False  # Volver al menú principal

        screen.blit(background_image, (0, 0))

        draw_text(screen, "Ranking", width // 2, height // 4 - 50, font_size["large"], colors["orange"], "center")

        if not scores:
            draw_text(screen, "No hay puntajes aún.", width // 2, height // 3, font_size["medium"], colors["white"], "center")
        else:
            draw_scores(screen, width, height // 3, font_size, colors, scores)

        draw_text(screen, "Presiona ESC o ENTER para volver", width // 2, height - 50, font_size["small"] - 12, colors["white"], "center")

        pygame.display.flip()


def draw_scores(screen: pygame.Surface, width: int, height: int, font_size: dict, colors: dict, scores: list[dict]) -> None:
    """
    Dibuja los puntajes ordenados en pantalla.
    """
    ordered_list_by_score = sort_list(scores, 'puntaje', 5)

    for i in range(len(ordered_list_by_score)):
        player = ordered_list_by_score[i]
        text = f"{i + 1}. {player['nombre']} - {player['puntaje']}"
        draw_text(screen, text, width // 2, height + i * 50, font_size["medium"], colors["white"], "center")
