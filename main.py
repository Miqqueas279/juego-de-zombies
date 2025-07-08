import sys
import json

import pygame

from screen.credits import show_credits
from screen.game import main_game_loop
from screen.menu import main_menu
from screen.ranking import show_ranking
from utils.score import load_scores, save_scores
from utils.soundtrack import stop_music

# --- Configuración Inicial de Pygame ---
pygame.init()
pygame.mixer.init() # Inicializar el mezclador de sonido para música y efectos

# --- Bucle Principal del Juego ---
def main():
    """
    Función principal que controla el flujo del juego entre el menú,
    la partida y el ranking.
    """
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    screen = pygame.display.set_mode((config["screen_size"]["width"], config["screen_size"]["height"]))
    pygame.display.set_caption("Cielo Letal") # Título de la ventana del juego

    running_main = True

    while running_main:
        # Mostrar el menú principal y obtener la opción seleccionada
        # Pasamos todas las variables de configuración necesarias
        option = main_menu(screen, config["screen_size"], config["font_size"], config["colors"])

        if option == "jugar":
            # Iniciar el bucle principal de la partida
            final_score, player_name = main_game_loop(screen, config["screen_size"], config["font_size"], config["colors"], config["player"], config["enemy"])
            
            # Si el juego terminó (no fue cerrado por el usuario con la X)
            if final_score is not None:
                # Cargar puntajes existentes, añadir el nuevo y guardarlos
                scores = load_scores()
                scores.append({"nombre": player_name, "puntaje": final_score})
                save_scores(scores)
                # Mostrar la pantalla de ranking después de guardar el puntaje
                show_ranking(screen, config["screen_size"], config["font_size"], config["colors"], scores)
        elif option == "ranking":
            # Cargar y mostrar el ranking
            scores = load_scores()
            show_ranking(screen, config["screen_size"], config["font_size"], config["colors"], scores)
        elif option == "creditos":
            stop_music()
            show_credits(screen, config["screen_size"], config["font_size"], config["colors"])
        elif option == "salir":
            running_main = False
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()