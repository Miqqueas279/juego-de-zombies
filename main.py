import pygame
import sys
import json
from screen.game import main_game_loop
from screen.menu import main_menu
from screen.ranking import show_ranking
from utils.score import load_scores, save_scores

# --- Configuración Inicial de Pygame ---
pygame.init()
pygame.mixer.init() # Inicializar el mezclador de sonido para música y efectos

# --- Configuración de Pantalla ---
#ANCHO_PANTALLA = 800
#ALTO_PANTALLA = 600
#PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
#pygame.display.set_caption("Cielo Letal") # Título de la ventana del juego

# --- Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
NARANJA = (228,142,0)

# --- Fuentes ---
# pygame.font.Font(None, tamaño) crea una fuente por defecto de Pygame
FUENTE_GRANDE = pygame.font.Font(None, 74)
FUENTE_MEDIA = pygame.font.Font(None, 50)
FUENTE_PEQUENA = pygame.font.Font(None, 36)

# --- Bucle Principal del Juego ---
def main():
    """
    Función principal que controla el flujo del juego entre el menú,
    la partida y el ranking.
    """
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    PANTALLA = pygame.display.set_mode((config["screen"]["width"], config["screen"]["height"]))
    pygame.display.set_caption("Cielo Letal") # Título de la ventana del juego

    while True:
        # Mostrar el menú principal y obtener la opción seleccionada
        # Pasamos todas las variables de configuración necesarias
        option = main_menu(PANTALLA, config["screen"]["width"], config["screen"]["height"], FUENTE_MEDIA, GRIS, NARANJA)

        if option == "jugar":
            # Iniciar el bucle principal de la partida
            puntaje_final, nombre_jugador = main_game_loop(PANTALLA, config["screen"]["width"], config["screen"]["height"], FUENTE_PEQUENA, NEGRO, BLANCO, ROJO, VERDE, AZUL)
            
            # Si el juego terminó (no fue cerrado por el usuario con la X)
            if puntaje_final is not None:
                # Cargar puntajes existentes, añadir el nuevo y guardarlos
                scores = load_scores()
                scores.append({"nombre": nombre_jugador, "puntaje": puntaje_final})
                save_scores(scores)
                # Mostrar la pantalla de ranking después de guardar el puntaje
                show_ranking(PANTALLA, config["screen"]["width"], config["screen"]["height"], FUENTE_GRANDE, FUENTE_MEDIA, NEGRO, BLANCO, scores)
        elif option == "ranking":
            # Cargar y mostrar el ranking
            scores = load_scores()
            show_ranking(PANTALLA, config["screen"]["width"], config["screen"]["height"], FUENTE_GRANDE, FUENTE_MEDIA, NEGRO, BLANCO, scores)
        elif option == "creditos":
            # Por ahora, un simple mensaje y vuelve al menú.
            print("Mostrar créditos (aún no implementado)")
        elif option == "salir":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()