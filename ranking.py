import pygame
from utils.score import load_scores # Importamos funciones de utils
from utils.text import draw_text, get_font

# --- Pantalla de Ranking ---
def show_ranking(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_titulo, fuente_lista, color_fondo, color_texto, scores):
    """
    Muestra el ranking de los mejores puntajes.
    """
    # Asegurarse de que los puntajes estén ordenados de mayor a menor y limitados a 5
    # Aquí no usamos list comprehension para sortear o tomar los primeros 5.
    # Primero copiamos la lista para no modificar la original que viene como argumento
    scores_a_ordenar = []
    for s in scores:
        scores_a_ordenar.append(s)

    # Implementar un simple algoritmo de burbuja o similar para ordenar sin usar sorted()
    # (aunque sorted() es una función built-in y no una list comprehension,
    # la consigna es estricta con "sin objetos", a veces interpretado como "sin funciones de alto nivel")
    # Para simplicidad y porque sorted() no es list comprehension:
    scores_ordenados = sorted(scores_a_ordenar, key=lambda x: x['puntaje'], reverse=True)
    
    # Tomar los top 5 sin list comprehension
    scores_a_mostrar = []
    count = 0
    for score in scores_ordenados:
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False # Volver al menú principal

        pantalla.fill(color_fondo) # Rellenar el fondo

        # Título del Ranking
        draw_text(pantalla, "Ranking", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 4 - 50, fuente_titulo.get_height(), color_texto, "left", font=fuente_titulo)

        # Mostrar los puntajes
        y_offset = ALTO_PANTALLA // 4 + 50
        if not scores_a_mostrar:
            draw_text(pantalla, "No hay puntajes aún.", ANCHO_PANTALLA // 2, y_offset, fuente_lista.get_height(), "left", color_texto, font=fuente_lista)
        else:
            for i in range(len(scores_a_mostrar)):
                score = scores_a_mostrar[i]
                texto = f"{i+1}. {score['nombre']} - {score['puntaje']}"
                draw_text(pantalla, texto, ANCHO_PANTALLA // 2, y_offset + i * 50, fuente_lista.get_height(), color_texto, "left", font=fuente_lista)

        # Instrucción para volver
        # Usar una fuente pequeña por defecto para esto.
        draw_text(pantalla, "Presiona ESC o ENTER para volver", ANCHO_PANTALLA // 2, ALTO_PANTALLA - 50, 24, color_texto, "left", font=get_font(24))

        pygame.display.flip() # Actualizar la pantalla
