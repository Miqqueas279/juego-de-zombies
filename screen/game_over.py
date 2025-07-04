import pygame
from utils.image import load_image
from utils.text import draw_text

def show_game_over(screen: pygame.Surface, screen_size: dict, font_size: dict, colors: dict, player: dict) -> tuple:
    name = ""
    input_active = True
    
    background_image = load_image("background.jpg", screen_size["width"], screen_size["height"], colors["black"])

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None # Si el usuario cierra la ventana durante el ingreso de nombre
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Si presiona ENTER, finaliza el ingreso
                    input_active = False
                elif event.key == pygame.K_BACKSPACE: # Si presiona BACKSPACE, borra el último carácter
                    name = name[:-1]
                else:
                    # Añadir el carácter presionado al nombre
                    name += event.unicode

        screen.blit(background_image, (0, 0))

        draw_text(screen, "GAME OVER", screen_size["width"] // 2, screen_size["height"] // 2 - 50, font_size["large"], colors["red"], "center")
        draw_text(screen, f"Puntaje Final: {player['puntos']}", screen_size["width"] // 2, screen_size["height"] // 2 + 20, font_size["small"], colors["white"], "center")
        draw_text(screen, "Ingresa tu nombre:", screen_size["width"] // 2, screen_size["height"] // 2 + 80, font_size["small"], colors["white"], "center")
        draw_text(screen, name + "|", screen_size["width"] // 2, screen_size["height"] // 2 + 120, font_size["small"], colors["white"], "center")
        
        pygame.display.flip()

    return player['puntos'], name