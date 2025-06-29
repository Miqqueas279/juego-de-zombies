import pygame
import os 

# Importamos funciones de utils
from utils.score import load_scores 
from utils.text import draw_text, get_font

# --- Pantalla de Ranking ---
def show_ranking(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_titulo, fuente_lista, color_fondo, color_texto, scores):
    """
    Muestra el ranking de los mejores puntajes.
    """
    # Asegurarse de que los puntajes estén ordenados de mayor a menor y limitados a 5
    # Primero copiamos la lista para no modificar la original que viene como argumento
    scores_a_ordenar = []
    for s in scores:
        scores_a_ordenar.append(s)

    # Algoritmo de burbuja para ordenar la lista de puntajes de mayor a menor
    # Esto sigue la preferencia de no usar funciones de alto nivel como sorted() si es posible.
    n = len(scores_a_ordenar)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if scores_a_ordenar[j]['puntaje'] < scores_a_ordenar[j+1]['puntaje']:
                scores_a_ordenar[j], scores_a_ordenar[j+1] = scores_a_ordenar[j+1], scores_a_ordenar[j]
    
    # Tomar los 5 mejores puntajes
    scores_a_mostrar = []
    count = 0
    for score in scores_a_ordenar:
        if count < 5:
            scores_a_mostrar.append(score)
            count += 1
        else:
            break

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                running = False # Volver al menú principal

        pantalla.fill(color_fondo) # Rellenar el fondo

        # Título del Ranking
        # Se usa "center" para la alineación horizontal del título.
        draw_text(pantalla, "Ranking", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 4 - 50, fuente_titulo.get_height(), color_texto, "center", font=fuente_titulo)

        # Mostrar los puntajes
        y_offset = ALTO_PANTALLA // 4 + 50
        if not scores_a_mostrar:
            # Se usa "center" para la alineación horizontal del mensaje.
            draw_text(pantalla, "No hay puntajes aún.", ANCHO_PANTALLA // 2, y_offset, fuente_lista.get_height(), color_texto, "center", font=fuente_lista)
        else:
            for i in range(len(scores_a_mostrar)):
                score = scores_a_mostrar[i]
                texto = f"{i+1}. {score['nombre']} - {score['puntaje']}"
                # Se usa "center" para la alineación horizontal de cada puntaje.
                draw_text(pantalla, texto, ANCHO_PANTALLA // 2, y_offset + i * 50, fuente_lista.get_height(), color_texto, "center", font=fuente_lista)

        # Instrucción para volver
        # Se usa "center" para la alineación horizontal.
        draw_text(pantalla, "Presiona ESC o ENTER para volver", ANCHO_PANTALLA // 2, ALTO_PANTALLA - 50, 24, color_texto, "center", font=get_font(24))

        pygame.display.flip() # Actualizar la pantalla
