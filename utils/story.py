import pygame

from utils.text import draw_text
from utils.image import load_image

# Líneas de la historia que se mostrarán al inicio del juego
story_lines = [
    "Eldoria sufre una oscura maldición.",
    "El Rey Theron ha desatado una plaga de zombis.",
    "El cielo rojo anuncia la tragedia.",
    "",
    "Sir Kaelen, un caballero exiliado, regresa con su espada y pistola.",
    "Su misión: llegar a Valoria y salvar el reino.",
    "",
    "Solo la Espada de la Luz puede romper el hechizo.",
    "El destino de Eldoria está en tus manos...",
]

def show_intro_story(screen: pygame.Surface, width: int, height: int, colors: dict[str, tuple[int, int, int]]) -> None:
    """
    Muestra una introducción animada con la historia del juego, línea por línea, con efecto de escritura.
    """
    background_image = load_image("trono vacio.jpg", width, height, colors["black"])
    clock = pygame.time.Clock()
    gray_color = (150, 150, 150)

    y_offset = 100
    spacing = 40
    running = True
    skip_story = False

    for line in story_lines:
        if skip_story:
            break

        text = ""
        for char in line:
            text += char
            screen.blit(background_image, (0, 0))

            # Dibujar líneas previas
            for idx, prev_line in enumerate(story_lines[:story_lines.index(line)]):
                draw_text(screen, prev_line, width // 2, 100 + idx * spacing, 28, colors["white"], "center")

            # Línea actual en progreso
            draw_text(screen, text, width // 2, y_offset, 28, colors["white"], "center")
            pygame.display.update()

            # Manejar eventos incluso durante la escritura
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        skip_story = True
                        break

            clock.tick(20)  # Controla la velocidad de escritura (20 FPS aprox.)

        y_offset += spacing
        clock.tick(1)  # Pequeña pausa entre líneas

    # Pantalla final si no se saltó
    if not skip_story:
        screen.blit(background_image, (0, 0))
        for idx, line in enumerate(story_lines):
            draw_text(screen, line, width // 2, 100 + idx * spacing, 28, colors["white"], "center")

        draw_text(screen, "Presiona Enter o Espacio para continuar...", width // 2, y_offset + 30, 24, gray_color, "center")
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        waiting = False
            clock.tick(30)
