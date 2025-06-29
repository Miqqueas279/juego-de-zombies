import pygame
import sys
# Importamos las funciones principales de cada módulo
from juego import main_game_loop
from menu import main_menu
from ranking import show_ranking
# Importamos load_scores y save_scores directamente desde utils.score
from utils.score import load_scores, save_scores 

# --- Configuración Inicial de Pygame ---
pygame.init()
pygame.mixer.init() # Inicializar el mezclador de sonido para música y efectos

# --- Configuración de Pantalla ---
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Cielo Letal") # Título de la ventana del juego

# --- Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO = (255, 0, 0) # Usado para "Dash CD"
VERDE = (0, 255, 0) # Usado para "Dash Listo"
AZUL = (0, 0, 255) # Usado para el jugador (si se necesitara un color)

# --- Fuentes ---
# pygame.font.Font(None, tamaño) crea una fuente por defecto de Pygame
# NOTA: Si deseas usar la fuente Zombies.otf aquí, deberías importarla desde utils.text
# Por ahora, usamos Font(None) como fallback seguro
FUENTE_GRANDE = pygame.font.Font(None, 74)
FUENTE_MEDIA = pygame.font.Font(None, 50)
FUENTE_PEQUENA = pygame.font.Font(None, 36) # Usada para UI del juego

# --- Bucle Principal del Juego ---
def main():
    """
    Función principal que controla el flujo del juego entre el menú,
    la partida y el ranking.
    """
    while True:
        # Mostrar el menú principal y obtener la opción seleccionada
        # Pasamos todas las variables de configuración necesarias al menú
        opcion_menu = main_menu(
            PANTALLA, ANCHO_PANTALLA, ALTO_PANTALLA, 
            FUENTE_GRANDE, FUENTE_MEDIA, NEGRO, # color_fondo_menu
            BLANCO, GRIS, VERDE, ROJO # Argumentos adicionales: color_opciones_normal, color_opcion_fondo_inactiva, color_opcion_seleccionada, color_borde_o_resaltado
        )

        if opcion_menu == "jugar":
            # Iniciar el bucle principal de la partida
            # El juego devuelve el puntaje final y el nombre del jugador
            puntaje_final, nombre_jugador = main_game_loop(
                PANTALLA, ANCHO_PANTALLA, ALTO_PANTALLA, 
                FUENTE_PEQUENA, NEGRO, BLANCO, ROJO, VERDE, AZUL # Colores y fuente para el juego
            )
            
            # Si el juego terminó (no fue cerrado por el usuario con la X)
            if puntaje_final is not None:
                # Cargar puntajes existentes, añadir el nuevo y guardarlos
                scores = load_scores()
                scores.append({"nombre": nombre_jugador, "puntaje": puntaje_final})
                save_scores(scores)
                # Mostrar la pantalla de ranking después de guardar el puntaje
                show_ranking(
                    PANTALLA, ANCHO_PANTALLA, ALTO_PANTALLA, 
                    FUENTE_GRANDE, FUENTE_MEDIA, NEGRO, BLANCO, scores # Colores y fuentes para el ranking
                )
        elif opcion_menu == "ranking":
            # Cargar y mostrar el ranking
            scores = load_scores()
            show_ranking(
                PANTALLA, ANCHO_PANTALLA, ALTO_PANTALLA, 
                FUENTE_GRANDE, FUENTE_MEDIA, NEGRO, BLANCO, scores # Colores y fuentes para el ranking
            )
        elif opcion_menu == "creditos":
            # TODO: Implementar la pantalla de créditos.
            print("Mostrar créditos (aún no implementado)")
        elif opcion_menu == "salir":
            # Si se selecciona "Salir", terminar Pygame y cerrar la aplicación
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
