import pygame
from utils import dibujar_texto, get_font # Importar funciones auxiliares y get_font

# --- Funciones para Botones (reemplazando la clase Boton) ---

def crear_boton_data(x, y, ancho, alto, texto, accion):
    """
    Crea un diccionario que representa los datos de un botón.
    """
    return {
        'rect': pygame.Rect(x, y, ancho, alto),
        'texto': texto,
        'accion': accion
    }

def dibujar_boton(pantalla, boton_data, mouse_pos, color_normal, color_hover, fuente_boton, color_texto):
    """
    Dibuja un botón en la pantalla, cambiando de color al pasar el mouse.
    """
    color_actual = color_hover if boton_data['rect'].collidepoint(mouse_pos) else color_normal
    pygame.draw.rect(pantalla, color_actual, boton_data['rect'], border_radius=10)
    dibujar_texto(pantalla, boton_data['texto'], boton_data['rect'].centerx, boton_data['rect'].centery, fuente_boton.get_height(), color_texto, fuente=fuente_boton)

def es_boton_clickeado(boton_data, mouse_pos):
    """
    Verifica si un botón ha sido clickeado.
    """
    return boton_data['rect'].collidepoint(mouse_pos)

# --- Menú Principal ---
def main_menu(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_titulo, fuente_boton, color_fondo, color_texto, color_boton_normal, color_boton_hover, color_borde):
    """
    Muestra el menú principal y maneja la interacción con los botones.
    Retorna la acción seleccionada ('jugar', 'ranking', 'creditos', 'salir').
    """
    # Lista de diccionarios de botones
    botones = [
        crear_boton_data(ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 - 80, 200, 60, "Jugar", "jugar"),
        crear_boton_data(ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2, 200, 60, "Ranking", "ranking"),
        crear_boton_data(ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 + 80, 200, 60, "Créditos", "creditos"),
        crear_boton_data(ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 + 160, 200, 60, "Salir", "salir")
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos() # Obtener la posición actual del mouse

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir" # Si el usuario cierra la ventana, salir del juego
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Click izquierdo del mouse
                    for boton in botones:
                        if es_boton_clickeado(boton, mouse_pos):
                            return boton['accion'] # Retornar la acción del botón clickeado

        pantalla.fill(color_fondo) # Rellenar el fondo de la pantalla

        # Dibujar el título del juego
        dibujar_texto(pantalla, "Cielo Letal", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 4, fuente_titulo.get_height(), color_texto, fuente=fuente_titulo)

        # Dibujar todos los botones
        for boton in botones:
            dibujar_boton(pantalla, boton, mouse_pos, color_boton_normal, color_boton_hover, fuente_boton, color_texto)

        pygame.display.flip() # Actualizar la pantalla
