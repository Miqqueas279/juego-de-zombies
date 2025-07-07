import pygame
import time
from utils.text import draw_text
from utils.image import load_image  # Importa tu función personalizada

# Historia breve y pausada
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

def show_intro_story(screen, width, height, font, colors):
    # Cargar imagen de fondo
    background_image = load_image("trono vacio.jpg", width, height, colors["black"])

    y_offset = 100
    spacing = 40

    for line in story_lines:
        for i in range(len(line) + 1):
            screen.blit(background_image, (0, 0))  # Dibujar el fondo

            # Dibujar líneas anteriores completas
            for idx, prev_line in enumerate(story_lines[:story_lines.index(line)]):
                draw_text(screen, prev_line, width // 2, 100 + idx * spacing, 28, colors["white"], "center")

            # Línea actual con efecto máquina de escribir
            partial = line[:i]
            draw_text(screen, partial, width // 2, y_offset, 28, colors["white"], "center")
            pygame.display.update()
            time.sleep(0.05)

        y_offset += spacing
        time.sleep(1)

    # Mensaje para continuar (con color gris definido directamente)
    gray_color = (150, 150, 150)
    draw_text(screen, "Presiona Enter o Espacio para continuar...", width // 2, y_offset + 30, 24, gray_color, "center")
    pygame.display.update()

    # Esperar tecla para continuar
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    waiting = False
