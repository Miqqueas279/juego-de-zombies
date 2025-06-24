import pygame
from utils import dibujar_texto, get_font # Importar funciones auxiliares y get_font

# --- Menú Principal ---
def main_menu(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_titulo, fuente_boton, color_fondo, color_texto, color_boton_normal, color_boton_hover, color_borde):
    """
    Muestra el menú principal y maneja la interacción con los botones.
    Retorna la acción seleccionada ('jugar', 'ranking', 'creditos', 'salir').
    """
    # Opciones del menú directamente en la función
    opciones = ["Jugar", "Ver Ranking", "Créditos", "Salir"]
    opcion_seleccionada = 0 # Índice de la opción actualmente seleccionada

    reloj = pygame.time.Clock()
    
    running = True
    while running:
        # Dibujar el fondo del menú
        pantalla.fill(color_fondo) # Usamos el color de fondo pasado como argumento

        # Dibujar el título del menú
        # Usamos fuente_titulo pasada como argumento
        dibujar_texto(pantalla, "🌟 MENÚ PRINCIPAL 🌟", ANCHO_PANTALLA // 2, 100, fuente_titulo.get_height(), color_texto, fuente=fuente_titulo)

        # Dibujar las opciones del menú
        for i, texto in enumerate(opciones):
            # Determinar el color de la opción: AZUL si está seleccionada, NEGRO si no
            # Usamos los colores pasados como argumentos
            color = color_boton_hover if i == opcion_seleccionada else color_texto
            # El texto se dibuja centrado
            dibujar_texto(pantalla, texto, ANCHO_PANTALLA // 2, 200 + i * 60, fuente_boton.get_height(), color, fuente=fuente_boton)

        pygame.display.flip() # Actualizar la pantalla para mostrar los cambios

        # --- Manejo de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir" # Si el usuario cierra la ventana, salir del juego
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    # Mover la selección hacia arriba, usando el operador módulo para ciclar
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    # Mover la selección hacia abajo, usando el operador módulo para ciclar
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    # Si se presiona ENTER, ejecutar la acción de la opción seleccionada
                    if opciones[opcion_seleccionada] == "Jugar":
                        return "jugar"
                    elif opciones[opcion_seleccionada] == "Ver Ranking":
                        return "ranking"
                    elif opciones[opcion_seleccionada] == "Créditos":
                        return "creditos"
                    elif opciones[opcion_seleccionada] == "Salir":
                        return "salir"

        reloj.tick(60) # Limitar a 60 FPS

