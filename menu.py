import pygame
from utils import dibujar_texto, get_font # Importar funciones auxiliares y get_font

# --- Menú Principal ---
def main_menu(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_titulo, fuente_boton, color_fondo, color_texto_normal, color_extra_unused_1, color_opcion_seleccionada, color_extra_unused_2):
    """
    Muestra el menú principal y maneja la interacción con los botones.
    Retorna la acción seleccionada ('jugar', 'ranking', 'creditos', 'salir').
    
    Parámetros:
    pantalla: La superficie de la pantalla de Pygame.
    ANCHO_PANTALLA, ALTO_PANTALLA: Dimensiones de la pantalla.
    fuente_titulo, fuente_boton: Objetos de fuente Pygame para el título y los botones.
    color_fondo: Color de fondo del menú.
    color_texto_normal: Color del texto de las opciones no seleccionadas (ej. BLANCO).
    color_extra_unused_1: Argumento adicional pasado desde main.py, no usado directamente en el menú de texto actual.
    color_opcion_seleccionada: Color del texto de la opción actualmente seleccionada (ej. VERDE).
    color_extra_unused_2: Argumento adicional pasado desde main.py, no usado directamente en el menú de texto actual.
    """
    # Opciones del menú
    opciones = ["Jugar", "Ver Ranking", "Créditos", "Salir"]
    opcion_seleccionada = 0 # Índice de la opción actualmente seleccionada

    reloj = pygame.time.Clock()
    
    running = True
    while running:
        # --- Manejo de Eventos ---
        # Este bucle es CRÍTICO para que Pygame procese las interacciones del usuario
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir" # Si el usuario cierra la ventana (botón X), salir del juego
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    # Mover la selección hacia arriba, ciclando entre las opciones
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    # Mover la selección hacia abajo, ciclando entre las opciones
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN: # Si se presiona ENTER
                    # Ejecutar la acción correspondiente a la opción seleccionada
                    if opciones[opcion_seleccionada] == "Jugar":
                        return "jugar"
                    elif opciones[opcion_seleccionada] == "Ver Ranking":
                        return "ranking"
                    elif opciones[opcion_seleccionada] == "Créditos":
                        return "creditos"
                    elif opciones[opcion_seleccionada] == "Salir":
                        return "salir"

        # --- Dibujo del Menú ---
        pantalla.fill(color_fondo) # Rellenar el fondo de la pantalla

        # Dibujar el título del menú
        # Se usa la fuente y el color de texto normales
        dibujar_texto(pantalla, "🌟 MENÚ PRINCIPAL 🌟", ANCHO_PANTALLA // 2, 100, fuente_titulo.get_height(), color_texto_normal, fuente=fuente_titulo)

        # Dibujar las opciones del menú
        for i, texto in enumerate(opciones):
            # Determinar el color de la opción:
            # Si está seleccionada, usar color_opcion_seleccionada
            # Si no está seleccionada, usar color_texto_normal
            color_opcion = color_opcion_seleccionada if i == opcion_seleccionada else color_texto_normal
            
            # El texto se dibuja centrado
            dibujar_texto(pantalla, texto, ANCHO_PANTALLA // 2, 200 + i * 60, fuente_boton.get_height(), color_opcion, fuente=fuente_boton)

        pygame.display.flip() # Actualizar la pantalla para mostrar los cambios

        # --- Control de FPS ---
        reloj.tick(60) # Limitar el bucle a 60 fotogramas por segundo
