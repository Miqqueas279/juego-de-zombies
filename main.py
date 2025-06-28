import pygame
import sys
# Importamos las funciones principales de cada módulo
from juego import main_game_loop
from menu import main_menu
from ranking import show_ranking
from utils import load_scores, save_scores # Las funciones de ranking ahora están en utils para simplificar las dependencias

print("main.py: Iniciando script...") # DEBUG

# --- Configuración Inicial de Pygame ---
pygame.init()
print("main.py: Pygame inicializado.") # DEBUG
pygame.mixer.init() # Inicializar el mezclador de sonido para música y efectos
print("main.py: Mixer de sonido inicializado.") # DEBUG

# --- Configuración de Pantalla ---
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Cielo Letal") # Título de la ventana del juego
print("main.py: Ventana de Pygame creada.") # DEBUG

# --- Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO = (255, 0, 0) # Usado para "Dash CD"
VERDE = (0, 255, 0) # Usado para "Dash Listo"
AZUL = (0, 0, 255) # Usado para el jugador

# --- Fuentes ---
FUENTE_GRANDE = pygame.font.Font(None, 74)
FUENTE_MEDIA = pygame.font.Font(None, 50)
FUENTE_PEQUENA = pygame.font.Font(None, 36) # Usada para UI del juego
print("main.py: Fuentes cargadas.") # DEBUG

# --- Bucle Principal del Juego ---
def main():
    """
    Función principal que controla el flujo del juego entre el menú,
    la partida y el ranking.
    """
    print("main.py: Entrando a la función main().") # DEBUG
    while True:
        print("main.py: Bucle principal del juego - Llamando a main_menu().") # DEBUG
        # Mostrar el menú principal y obtener la opción seleccionada
        opcion_menu = main_menu(
            PANTALLA, ANCHO_PANTALLA, ALTO_PANTALLA, 
            FUENTE_GRANDE, FUENTE_MEDIA, NEGRO, # color_fondo_menu
            BLANCO, GRIS, VERDE, ROJO # color_opciones_normal, color_opcion_fondo_inactiva, color_opcion_seleccionada, color_borde_o_resaltado
        )
        print(f"main.py: main_menu() retornó: {opcion_menu}") # DEBUG

        if opcion_menu == "jugar":
            print("main.py: Opción 'Jugar' seleccionada. Iniciando main_game_loop().") # DEBUG
            # Iniciar el bucle principal de la partida
            puntaje_final, nombre_jugador = main_game_loop(
                PANTALLA, ANCHO_PANTALLA, ALTO_PANTALLA, 
                FUENTE_PEQUENA, NEGRO, BLANCO, ROJO, VERDE, AZUL # Colores y fuente para el juego
            )
            print(f"main.py: main_game_loop() finalizado. Puntaje: {puntaje_final}, Nombre: {nombre_jugador}") # DEBUG
            
            # Si el juego terminó (no fue cerrado por el usuario con la X)
            if puntaje_final is not None:
                print("main.py: Guardando y mostrando ranking.") # DEBUG
                # Cargar puntajes existentes, añadir el nuevo y guardarlos
                scores = load_scores()
                scores.append({"nombre": nombre_jugador, "puntaje": puntaje_final})
                save_scores(scores)
                # Mostrar la pantalla de ranking después de guardar el puntaje
                show_ranking(
                    PANTALLA, ANCHO_PANTALLA, ALTO_PANTALLA, 
                    FUENTE_GRANDE, FUENTE_MEDIA, NEGRO, BLANCO, scores # Colores y fuentes para el ranking
                )
                print("main.py: Ranking mostrado.") # DEBUG
        elif opcion_menu == "ranking":
            print("main.py: Opción 'Ranking' seleccionada. Mostrando ranking.") # DEBUG
            # Cargar y mostrar el ranking
            scores = load_scores()
            show_ranking(
                PANTALLA, ANCHO_PANTALLA, ALTO_PANTALLA, 
                FUENTE_GRANDE, FUENTE_MEDIA, NEGRO, BLANCO, scores # Colores y fuentes para el ranking
            )
            print("main.py: Ranking mostrado.") # DEBUG
        elif opcion_menu == "creditos":
            print("main.py: Opción 'Créditos' seleccionada. (Implementación pendiente).") # DEBUG
            # TODO: Implementar la pantalla de créditos.
            print("Mostrar créditos (aún no implementado)")
        elif opcion_menu == "salir":
            print("main.py: Opción 'Salir' seleccionada. Cerrando Pygame.") # DEBUG
            # Si se selecciona "Salir", terminar Pygame y cerrar la aplicación
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
    print("main.py: Script finalizado.") # DEBUG
