import pygame
import math
import os # Importar os para manejar rutas de archivos

from entities.enemy import dibujar_enemigos, generar_enemigo, mover_enemigos
from entities.player import actualizar_dash_jugador, dibujar_disparos, dibujar_jugador, disparar_jugador, init_player, mover_disparos, mover_jugador, usar_dash_jugador
from utils.score import detectar_colision_rect # Importar funciones auxiliares
from utils.text import draw_text, get_font

# --- Constantes del Juego ---
GREEN = (0, 255, 0)

# Nuevo color para los corazones "vacíos" (vidas perdidas)
COLOR_CORAZON_PERDIDO = (50, 50, 50, 150) # Gris oscuro semi-transparente (con transparencia)

VIDAS_INICIALES = 3
# Frecuencia de generación de enemigos
COOLDOWN_GENERACION_ENEMIGO_FRAMES = 60 # Aproximadamente 1 enemigo por segundo a 60 FPS
# Rutas de imágenes
# Obtener el directorio base del script actual
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Cargamos la spritesheet completa 'icons.png'
SPRITESHEET_ICONS_PATH = os.path.join(BASE_DIR, 'assets\\image', 'icons.png') 

# --- Funciones de Manejo de Entidades ---
def limpiar_entidades_fuera_pantalla(enemigos_list, disparos_list, ALTO_PANTALLA):
    """
    Elimina enemigos y disparos que han salido de la pantalla.
    Iteramos hacia atrás para poder eliminar elementos de la lista sin problemas de índice.
    """
    # Limpiar enemigos
    i = len(enemigos_list) - 1
    while i >= 0:
        if enemigos_list[i]['rect'].top > ALTO_PANTALLA:
            del enemigos_list[i]
        i -= 1
    
    # Limpiar disparos (del jugador, que van hacia arriba)
    i = len(disparos_list) - 1
    while i >= 0:
        if disparos_list[i]['rect'].bottom < 0:
            del disparos_list[i]
        i -= 1

def manejar_colisiones(player_data, enemigos_list, player_bullets_list):
    """
    Maneja todas las colisiones entre entidades y actualiza vidas/puntos.
    Retorna True si el juego termina (vidas del jugador <= 0), False en caso contrario.
    """
    game_over = False

    player_impact_sound = pygame.mixer.Sound("assets\\sounds\\impact.mp3")
    player_impact_sound.set_volume(0.3)
    enemy_impact_sound = pygame.mixer.Sound("assets\\sounds\\enemy_impact.mp3")
    enemy_impact_sound.set_volume(0.1) 

    # Colisión disparos del jugador con enemigos
    i_bullet = len(player_bullets_list) - 1
    while i_bullet >= 0:
        bullet = player_bullets_list[i_bullet]
        j_enemy = len(enemigos_list) - 1
        bullet_hit = False # Bandera para saber si la bala impactó
        while j_enemy >= 0:
            enemy = enemigos_list[j_enemy]
            if detectar_colision_rect(bullet['rect'], enemy['rect']):
                enemy['vida'] -= 1
                enemy_impact_sound.play()
                bullet_hit = True # La bala impactó, debe ser eliminada
                if enemy['vida'] <= 0:
                    player_data['puntos'] += enemy['puntos'] # Sumar puntos por enemigo destruido
                    del enemigos_list[j_enemy] # Eliminar enemigo
                break # Salir del bucle interno, el disparo ya impactó
            j_enemy -= 1
        
        if bullet_hit:
            del player_bullets_list[i_bullet] # Eliminar el disparo
        i_bullet -= 1

    # Colisión enemigo con jugador
    i_enemy = len(enemigos_list) - 1
    while i_enemy >= 0:
        enemy = enemigos_list[i_enemy]
        if detectar_colision_rect(player_data['rect'], enemy['rect']):
            player_data['vidas'] -= 1
            player_impact_sound.play()
            del enemigos_list[i_enemy] # El enemigo se destruye al impactar al jugador
            if player_data['vidas'] <= 0:
                game_over = True # Juego terminado
                break # No es necesario seguir revisando enemigos
        i_enemy -= 1
    
    return game_over

def dibujar_vidas_corazones(pantalla, vidas_actuales, vidas_maximas, heart_image_surface, lost_heart_color):
    """
    Dibuja los corazones de vida al estilo Minecraft.
    """
    x_offset = 10 # Posición inicial X para el primer corazón
    y_offset = 40 # Posición Y para los corazones
    spacing = heart_image_surface.get_width() + 5 # Espacio entre corazones

    for i in range(vidas_maximas):
        if i < vidas_actuales:
            # Dibujar corazón rojo (vida actual)
            pantalla.blit(heart_image_surface, (x_offset + i * spacing, y_offset))
        else:
            # Dibujar un rectángulo gris oscuro semi-transparente para la vida perdida
            lost_heart_rect = pygame.Rect(x_offset + i * spacing, y_offset, 
                                          heart_image_surface.get_width(), 
                                          heart_image_surface.get_height()) 
            s = pygame.Surface(lost_heart_rect.size, pygame.SRCALPHA) # Superficie con canal alfa
            s.fill(lost_heart_color) # Rellenar con el color gris oscuro semi-transparente
            pantalla.blit(s, lost_heart_rect)


# --- Bucle Principal del Juego (main_game_loop) ---
def main_game_loop(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_pequena, NEGRO, BLANCO, ROJO, VERDE, AZUL):
    """
    Gestiona la lógica principal de la partida.
    Retorna el puntaje final y el nombre del jugador si el juego termina.
    """
    FONDO_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'floor.jpg')
    fondo_surface = pygame.image.load(FONDO_PATH).convert()
    fondo_surface = pygame.transform.scale(fondo_surface, (ANCHO_PANTALLA, ALTO_PANTALLA))

    PLAYER_IMAGE_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'player.png')
    ENEMY_IMAGE_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'zombie.png')

    player_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
    enemy_image = pygame.image.load(ENEMY_IMAGE_PATH).convert_alpha()

# Escalar imágenes al tamaño del rectángulo
    player_image = pygame.transform.scale(player_image, (50, 50))  # Tamaño del jugador
    enemy_image = pygame.transform.scale(enemy_image, (40, 40))

    shoot_sound = pygame.mixer.Sound("assets\\sounds\\player_shoot.mp3")
    shoot_sound.set_volume(0.1)

    # Variable local para la superficie del corazón
    heart_surface_local = None 

    # Cargar y procesar la imagen del corazón una vez
    # Esta variable local se inicializará la primera vez que se llama a main_game_loop
    # y mantendrá su valor en llamadas subsecuentes dentro de la misma ejecución del juego.
    if heart_surface_local is None:
        try:
            # Cargar la spritesheet completa
            spritesheet = pygame.image.load(SPRITESHEET_ICONS_PATH).convert_alpha()

            # Definir el rectángulo del corazón lleno en la spritesheet (x, y, ancho, alto)
            # El corazón rojo completo está en (16,0) y mide 9x9 píxeles en la spritesheet de Minecraft
            HEART_SPRITE_RECT_SOURCE = pygame.Rect(52, 0, 9, 9) #(el 52 marca la posicion donde esta el corazon rojo 
            #                                                    del spirtesheet de minecraft, si lo quieren cambiar a 
            #                                                    alguno vayan probando numeros) 

            # Extraer el corazón lleno
            heart_surface_local = spritesheet.subsurface(HEART_SPRITE_RECT_SOURCE)
            
            # Escalar el corazón para que sea más visible
            SCALE_SIZE = (30, 30) # Tamaño deseado para los corazones en pantalla
            heart_surface_local = pygame.transform.scale(heart_surface_local, SCALE_SIZE)

        except pygame.error as e:
            print(f"Error cargando o procesando la spritesheet de iconos: {e}")
            # Fallback si no se puede cargar o procesar la imagen: un círculo rojo
            temp_surface_full = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface_full, (255, 0, 0, 255), (15, 15), 15) # Círculo rojo opaco
            heart_surface_local = temp_surface_full


    reloj = pygame.time.Clock()
    fps = 60

    # Inicializar datos del jugador
    player = init_player(ANCHO_PANTALLA, ALTO_PANTALLA)
    
    # Listas para guardar enemigos y disparos
    enemigos = []
    player_bullets = []

    frames_desde_ultima_generacion_enemigo = 0 # Contador para la generación de enemigos

    running = True
    while running:
        # Obtener el tiempo actual en frames (o ticks)
        current_frames = pygame.time.get_ticks() // (1000 // fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None, None # Si el usuario cierra la ventana durante el juego
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Intentar disparar y añadir el nuevo disparo a la lista
                    nuevo_disparo = disparar_jugador(player, current_frames)
                    if nuevo_disparo:
                        shoot_sound.play()
                        player_bullets.append(nuevo_disparo)
                if event.key == pygame.K_z: # Tecla para el dash
                    usar_dash_jugador(player)

        # --- Movimiento del Jugador ---
        keys = pygame.key.get_pressed() # Obtener todas las teclas presionadas
        mover_jugador(player, keys, ANCHO_PANTALLA)
        actualizar_dash_jugador(player) # Actualizar el temporizador del dash

        # --- Generación de Enemigos ---
        frames_desde_ultima_generacion_enemigo += 1
        if frames_desde_ultima_generacion_enemigo >= COOLDOWN_GENERACION_ENEMIGO_FRAMES:
            enemigos.append(generar_enemigo(ANCHO_PANTALLA))
            frames_desde_ultima_generacion_enemigo = 0 # Reiniciar el contador

        # --- Movimiento de Enemigos y Disparos ---
        mover_enemigos(enemigos)
        mover_disparos(player_bullets)

        # --- Colisiones ---
        # La función de colisiones también elimina los objetos impactados y actualiza puntos/vidas
        game_over = manejar_colisiones(player, enemigos, player_bullets)
        if game_over:
            running = False # Si el jugador pierde todas las vidas, terminar el juego

        # --- Eliminar elementos fuera de pantalla ---
        limpiar_entidades_fuera_pantalla(enemigos, player_bullets, ALTO_PANTALLA)

        # --- Dibujar ---
        pantalla.blit(fondo_surface, (0, 0))

        dibujar_jugador(pantalla, player, player_image, AZUL, BLANCO) # Dibujar el jugador
        dibujar_enemigos(pantalla, enemigos, enemy_image) # Dibujar todos los enemigos
        dibujar_disparos(pantalla, player_bullets) # Dibujar todos los disparos del jugador

        # Dibujar UI (vidas y puntaje)
        draw_text(pantalla, f"Puntaje: {player['puntos']}", 15, 20, 24, BLANCO, "left")
        # Reemplazar el texto de vidas con los corazones
        # Pasamos el corazón rojo y el color para los corazones perdidos
        dibujar_vidas_corazones(pantalla, player['vidas'], VIDAS_INICIALES, heart_surface_local, COLOR_CORAZON_PERDIDO)
        
        # Mostrar el estado del dash cooldown
        if player['dash_cooldown_timer'] > 0:
            tiempo_restante_dash = math.ceil(player['dash_cooldown_timer'] / fps)
            draw_text(pantalla, f"Dash CD: {tiempo_restante_dash}s", ANCHO_PANTALLA - 150, 10, 24, ROJO, "left")
        elif not player['en_dash']:
            draw_text(pantalla, "Dash Listo", ANCHO_PANTALLA - 110, 20, 24, VERDE, "left")


        pygame.display.flip() # Actualizar toda la pantalla

        reloj.tick(fps) # Controlar los FPS del juego

    # --- Game Over Screen ---
    # Pedir nombre al jugador después de que el bucle principal del juego termina
    nombre_ingresado = ""
    input_activo = True

    while input_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None # Si el usuario cierra la ventana durante el ingreso de nombre
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Si presiona ENTER, finaliza el ingreso
                    input_activo = False
                elif event.key == pygame.K_BACKSPACE: # Si presiona BACKSPACE, borra el último carácter
                    nombre_ingresado = nombre_ingresado[:-1]
                else:
                    # Añadir el carácter presionado al nombre
                    nombre_ingresado += event.unicode

        pantalla.fill(NEGRO) # Fondo negro para la pantalla de Game Over
        draw_text(pantalla, "GAME OVER", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 50, 74, ROJO, "center")
        draw_text(pantalla, f"Puntaje Final: {player['puntos']}", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 20, 36, BLANCO, "center")
        draw_text(pantalla, "Ingresa tu nombre:", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 80, 36, BLANCO, "center")
        # Mostrar el nombre ingresado y un cursor simulado
        draw_text(pantalla, nombre_ingresado + "|", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 120, 36, BLANCO, "center")
        pygame.display.flip()

    return player['puntos'], nombre_ingresado # Devolver el puntaje y el nombre para guardar
