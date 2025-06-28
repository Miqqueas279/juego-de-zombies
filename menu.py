import pygame
from utils import dibujar_texto, get_font # Importar funciones auxiliares y get_font

# --- Menú Principal ---
def main_menu(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_titulo, fuente_boton, color_fondo_menu, color_opciones_normal, color_opcion_fondo_inactiva, color_opcion_seleccionada, color_borde_o_resaltado):
    """
    Muestra el menú principal y maneja la interacción con los botones.
    Retorna la acción seleccionada ('jugar', 'ranking', 'creditos', 'salir').
    
    Parámetros:
    pantalla: La superficie de la pantalla de Pygame.
    ANCHO_PANTALLA, ALTO_PANTALLA: Dimensiones de la pantalla.
    fuente_titulo, fuente_boton: Objetos de fuente Pygame para el título y los botones.
    color_fondo_menu: Color de fondo del menú (ej. NEGRO).
    color_opciones_normal: Color del texto de las opciones no seleccionadas (ej. BLANCO).
    color_opcion_fondo_inactiva: Color para el fondo de opciones inactivas (ej. GRIS). No se usa directamente en este menú basado en texto.
    color_opcion_seleccionada: Color del texto de la opción actualmente seleccionada (ej. VERDE).
    color_borde_o_resaltado: Color para bordes o resaltados (ej. ROJO). No se usa directamente en este menú basado en texto.
    """
    print("menu.py: Entrando a main_menu().") # DEBUG
    opciones = ["Jugar", "Ver Ranking", "Créditos", "Salir"]
    opcion_seleccionada = 0

    reloj = pygame.time.Clock()
    
    running = True
    while running:
        # --- Manejo de Eventos ---
        # Este bucle es CRÍTICO para que Pygame procese las interacciones del usuario
        for evento in pygame.event.get():
            print(f"menu.py: Procesando evento: {evento.type}") # DEBUG
            if evento.type == pygame.QUIT:
                print("menu.py: Evento QUIT detectado.") # DEBUG
                return "salir"
            elif evento.type == pygame.KEYDOWN: # <--- ¡IMPORTANTE! Detectamos que ES una tecla presionada
                print(f"menu.py: *** Tecla KEYDOWN detectada! Codigo: {evento.key} ***") # DEBUG MUY IMPORTANTE
                if evento.key == pygame.K_UP:
                    # Mover la selección hacia arriba, ciclando entre las opciones
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                    print(f"menu.py: Selección cambiada a: {opciones[opcion_seleccionada]}") # DEBUG
                elif evento.key == pygame.K_DOWN:
                    # Mover la selección hacia abajo, ciclando entre las opciones
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                    print(f"menu.py: Selección cambiada a: {opciones[opcion_seleccionada]}") # DEBUG
                elif evento.key == pygame.K_RETURN:
                    print(f"menu.py: ENTER presionado. Opción seleccionada: {opciones[opcion_seleccionada]}") # DEBUG
                    if opciones[opcion_seleccionada] == "Jugar":
                        return "jugar"
                    elif opciones[opcion_seleccionada] == "Ver Ranking":
                        return "ranking"
                    elif opciones[opcion_seleccionada] == "Créditos":
                        return "creditos"
                    elif opciones[opcion_seleccionada] == "Salir":
                        return "salir"

        # --- Dibujo del Menú ---
        pantalla.fill(color_fondo_menu)

        dibujar_texto(pantalla, "🌟 MENÚ PRINCIPAL 🌟", ANCHO_PANTALLA // 2, 100, fuente_titulo.get_height(), color_opciones_normal, fuente=fuente_titulo)

        for i, texto in enumerate(opciones):
            color_opcion = color_opcion_seleccionada if i == opcion_seleccionada else color_opciones_normal
            dibujar_texto(pantalla, texto, ANCHO_PANTALLA // 2, 200 + i * 60, fuente_boton.get_height(), color_opcion, fuente=fuente_boton)

        pygame.display.flip()

        reloj.tick(60)
