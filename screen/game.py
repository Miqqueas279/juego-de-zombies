import pygame
import math
import json
import os # Importar os para manejar rutas de archivos
from entities.powerup import crear_powerup, mover_powerups, dibujar_powerups, recoger_powerups

from entities.enemy import dibujar_enemigos, generar_enemigo, mover_enemigos, ZOMBIE_FRAME_WIDTH, ZOMBIE_FRAME_HEIGHT # Importar constantes de animación
from entities.player import actualizar_dash_jugador, dibujar_disparos, dibujar_jugador, disparar_jugador, init_player, mover_disparos, mover_jugador, usar_dash_jugador, PLAYER_FRAME_WIDTH, PLAYER_FRAME_HEIGHT, PLAYER_TOTAL_FRAMES_PER_ROW # Importar constantes de animación del jugador
from screen.game_over import show_game_over # Asumo que esta función existe en screen/game_over.py
from utils.collision import detectar_colision_rect # Importar funciones auxiliares desde el módulo correcto
from utils.soundtrack import play_music, load_sound
from utils.text import draw_text, get_font

# --- Constantes del Juego ---
GREEN = (0, 255, 0)

VIDAS_INICIALES = 3
VIDAS_MAXIMAS = 5
COLOR_CORAZON_PERDIDO = (50, 50, 50, 150) 
# Frecuencia de generación de enemigos
COOLDOWN_GENERACION_ENEMIGO_FRAMES = 60 # Aproximadamente 1 enemigo por segundo a 60 FPS

# Rutas de imágenes
# Obtener el directorio base del script actual
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Cargamos la spritesheet completa 'icons.png'
SPRITESHEET_ICONS_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'icons.png') 

# Rutas de las spritesheets de zombies
ZOMBIE_NORMAL_SPRITESHEET_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'zombie1.PNG') # Zombie normal
ZOMBIE_BOOSTED_SPRITESHEET_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'zombie2.PNG') # Zombie boosted
ZOMBIE_KAMIKAZE_SPRITESHEET_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'zombie3.PNG') # Zombie kamikaze

# Ruta de la spritesheet del jugador
PLAYER_SPRITESHEET_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'prota1.PNG') 


# --- Funciones de Manejo de Entidades ---
def limpiar_entidades_fuera_pantalla(enemigos_list: list, disparos_list: list, powerups_list: list, ANCHO_PANTALLA: int) -> None:
    """
    Elimina enemigos, disparos y power-ups que han salido de la pantalla en un juego horizontal.
    Iteramos hacia atrás para poder eliminar elementos de la lista sin problemas de índice.
    """
    # Limpiar enemigos (que se mueven de derecha a izquierda)
    i = len(enemigos_list) - 1
    while i >= 0:
        # Si el enemigo ha salido completamente por la izquierda
        if enemigos_list[i]['rect'].right < 0:
            del enemigos_list[i]
        i -= 1
    
    # Limpiar disparos (del jugador, que van hacia la derecha)
    i = len(disparos_list) - 1
    while i >= 0:
        # Si el disparo ha salido completamente por la derecha
        if disparos_list[i]['rect'].left > ANCHO_PANTALLA:
            del disparos_list[i]
        i -= 1
    
    # Limpiar power-ups (que se mueven de derecha a izquierda y ya no están activos)
    temp_powerups_list = []
    i = 0
    while i < len(powerups_list):
        if powerups_list[i]['activo'] and powerups_list[i]['rect'].right > 0:
            temp_powerups_list.append(powerups_list[i])
        i += 1
    # Asignar la lista filtrada de vuelta
    powerups_list[:] = temp_powerups_list # Esto modifica la lista original en su lugar


def manejar_colisiones(player_data, enemigos_list, player_bullets_list, lost_health_sound: pygame.mixer.Sound | None, player_impact_sound: pygame.mixer.Sound | None, enemy_impact_sound: pygame.mixer.Sound | None):
    """
    Detecta colisiones entre jugador, enemigos y balas.
    Devuelve True si el jugador pierde todas las vidas.
    """
    # Colisiones disparos vs enemigos
    i = len(player_bullets_list) - 1
    while i >= 0:
        bullet = player_bullets_list[i]
        j = len(enemigos_list) - 1
        while j >= 0:
            enemy = enemigos_list[j]
            if detectar_colision_rect(bullet['rect'], enemy['rect']):
                enemy['vida'] -= 1
                if enemy_impact_sound:
                    enemy_impact_sound.play()
                if enemy['vida'] <= 0:
                    player_data['puntos'] += enemy['puntos']
                    del enemigos_list[j]
                del player_bullets_list[i]
                break
            j -= 1
        i -= 1

    # Colisiones enemigos vs jugador
    i = len(enemigos_list) - 1
    while i >= 0:
        enemy = enemigos_list[i]
        if detectar_colision_rect(player_data['rect'], enemy['rect']):
            player_data['vidas'] -= 1
            if player_impact_sound:
                player_impact_sound.play()
            if lost_health_sound:
                lost_health_sound.play()
            del enemigos_list[i]
            print(f"[DEBUG] Vidas restantes: {player_data['vidas']}")
            if player_data['vidas'] <= 0:
                print("[DEBUG] Jugador sin vidas. Fin del juego.")
                return True
        i -= 1

    return False

def dibujar_vidas_corazones(pantalla: pygame.Surface, vidas_actuales: int, vidas_maximas: int, heart_image_surface: pygame.Surface, lost_heart_color: tuple) -> None:
    """
    Dibuja corazones llenos y vacíos hasta VIDAS_MAXIMAS.
    """
    x_offset = 10
    y_offset = 40
    spacing = heart_image_surface.get_width() + 5

    for i in range(vidas_maximas): # Iterar hasta VIDAS_MAXIMAS
        x = x_offset + i * spacing
        if i < vidas_actuales:
            pantalla.blit(heart_image_surface, (x, y_offset))
        else:
            s = pygame.Surface(heart_image_surface.get_size(), pygame.SRCALPHA)
            s.fill(lost_heart_color)
            pantalla.blit(s, (x, y_offset))


# --- Bucle Principal del Juego (main_game_loop) ---
def main_game_loop(pantalla: pygame.Surface, ANCHO_PANTALLA: int, ALTO_PANTALLA: int, fuente_pequena: pygame.font.Font, NEGRO: tuple, BLANCO: tuple, ROJO: tuple, VERDE: tuple, AZUL: tuple) -> tuple:
    """
    Gestiona la lógica principal de la partida.
    Retorna el puntaje final y el nombre del jugador si el juego termina.
    """
    FONDO_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'floor.jpg')
    fondo_surface = pygame.image.load(FONDO_PATH).convert()
    fondo_surface = pygame.transform.scale(fondo_surface, (ANCHO_PANTALLA, ALTO_PANTALLA))

    play_music("game_music.mp3", 0.05)

    # Cargar la spritesheet del jugador
    player_spritesheet = pygame.image.load(PLAYER_SPRITESHEET_PATH).convert_alpha()
    player_spritesheet = pygame.transform.scale(player_spritesheet, (PLAYER_FRAME_WIDTH * PLAYER_TOTAL_FRAMES_PER_ROW, PLAYER_FRAME_HEIGHT * 4)) 

    powerup_imagenes = {
        'vida': pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, 'assets', 'image', 'powerup_vida.png')), (30, 30)),
        'velocidad': pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, 'assets', 'image', 'powerup_velocidad.png')), (30, 30))
    }
    
    # Cargar las spritesheets de zombies para cada tipo
    zombie_spritesheets = {
        "normal": pygame.image.load(ZOMBIE_NORMAL_SPRITESHEET_PATH).convert_alpha(),
        "boosted": pygame.image.load(ZOMBIE_BOOSTED_SPRITESHEET_PATH).convert_alpha(),
        "kamikaze": pygame.image.load(ZOMBIE_KAMIKAZE_SPRITESHEET_PATH).convert_alpha()
    }

    for tipo in zombie_spritesheets:
        zombie_spritesheets[tipo] = pygame.transform.scale(zombie_spritesheets[tipo], 
                                                           (ZOMBIE_FRAME_WIDTH * 3, ZOMBIE_FRAME_HEIGHT * 4)) # Asumiendo 3x4 frames por spritesheet
        
    shoot_sound = load_sound("player_shoot.mp3", 0.1)
    recover_health_sound = load_sound("recover_health.mp3", 0.4)
    lost_health_sound = load_sound("lost_health.mp3", 0.4)
    increase_speed_sound = load_sound("increase_speed.mp3", 0.4)
    player_impact_sound = load_sound("player_impact.mp3", 0.3)
    enemy_impact_sound = load_sound("enemy_impact.mp3", 0.1)

    # Cargar y procesar la imagen del corazón una vez 
    spritesheet_icons = pygame.image.load(SPRITESHEET_ICONS_PATH).convert_alpha() 

    # Definir el rectángulo del corazón lleno en la spritesheet (x, y, ancho, alto)
    HEART_SPRITE_RECT_SOURCE = pygame.Rect(52, 0, 9, 9) 

    # Extraer el corazón lleno
    heart_surface_local = spritesheet_icons.subsurface(HEART_SPRITE_RECT_SOURCE) 
    
    # Escalar el corazón para que sea más visible
    SCALE_SIZE = (30, 30) # Tamaño deseado para los corazones en pantalla
    heart_surface_local = pygame.transform.scale(heart_surface_local, SCALE_SIZE)


    reloj = pygame.time.Clock()
    fps = 60 # Definir FPS aquí o cargar desde config.json

    # Inicializar datos del jugador
    player = init_player(ANCHO_PANTALLA, ALTO_PANTALLA)
    
    # Listas para guardar enemigos y disparos
    enemigos = []
    player_bullets = []
    powerups = [] # Lista para los power-ups

    frames_desde_ultima_generacion_enemigo = 0 # Contador para la generación de enemigos
    frames_para_nuevo_powerup = 0
    POWERUP_INTERVALO_FRAMES = 600  # cada 10 segundos (60 FPS * 10)


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
                        if shoot_sound:
                            shoot_sound.play()
                        player_bullets.append(nuevo_disparo)
                if event.key == pygame.K_z: # Tecla para el dash
                    usar_dash_jugador(player)

        # --- Movimiento del Jugador ---
        keys = pygame.key.get_pressed()
        mover_jugador(player, keys, ALTO_PANTALLA)
        actualizar_dash_jugador(player) # Actualizar el temporizador del dash

        # --- Generación de Power-ups ---
        frames_para_nuevo_powerup += 1
        if frames_para_nuevo_powerup >= POWERUP_INTERVALO_FRAMES:
            powerups.append(crear_powerup(ANCHO_PANTALLA, ALTO_PANTALLA))
            frames_para_nuevo_powerup = 0
        
        # --- Generación de Enemigos ---
        frames_desde_ultima_generacion_enemigo += 1
        if frames_desde_ultima_generacion_enemigo >= COOLDOWN_GENERACION_ENEMIGO_FRAMES:
            enemigos.append(generar_enemigo(ANCHO_PANTALLA, ALTO_PANTALLA))
            frames_desde_ultima_generacion_enemigo = 0 # Reiniciar el contador

        # --- Movimiento de Entidades ---
        mover_enemigos(enemigos, player)
        mover_disparos(player_bullets)
        mover_powerups(powerups) # Mover los power-ups

        # --- Colisiones ---
        # Manejar colisiones entre jugador/enemigos/disparos
        game_over = manejar_colisiones(player, enemigos, player_bullets, lost_health_sound, player_impact_sound, enemy_impact_sound)
        if game_over:
            running = False # Si el jugador pierde todas las vidas, terminar el juego

        # Manejar colisiones entre jugador y power-ups
        for i in range(len(powerups) - 1, -1, -1):
            powerup = powerups[i]
            if player['rect'].colliderect(powerup['rect']):
                if powerup['tipo'] == 'vida' and player['vidas'] < VIDAS_MAXIMAS:
                    player['vidas'] += 1
                    if recover_health_sound:
                        recover_health_sound.play()
                elif powerup['tipo'] == 'velocidad':
                    player['velocidad'] += 1
                    if increase_speed_sound:
                        increase_speed_sound.play()
                del powerups[i] # Pasar VIDAS_MAXIMAS


        # --- Eliminar elementos fuera de pantalla ---
        # Ahora pasamos la lista de power-ups también
        limpiar_entidades_fuera_pantalla(enemigos, player_bullets, powerups, ANCHO_PANTALLA)


        # --- Dibujar ---
        pantalla.blit(fondo_surface, (0, 0))

        # Ahora pasamos la spritesheet del jugador a dibujar_jugador
        dibujar_jugador(pantalla, player, player_spritesheet, AZUL, BLANCO) 
        # Ahora pasamos el diccionario de spritesheets de zombies a dibujar_enemigos
        dibujar_enemigos(pantalla, enemigos, zombie_spritesheets) 
        dibujar_disparos(pantalla, player_bullets) # Dibujar todos los disparos del jugador
        dibujar_powerups(pantalla, powerups, powerup_imagenes) # Dibujar los power-ups

        # Dibujar UI (vidas y puntaje)
        # Ajustar posición del puntaje para el layout horizontal
        draw_text(pantalla, f"Puntaje: {player['puntos']}\n", 15, 20, 24, BLANCO, "left") # Agregué un salto de línea para separar del dash CD
        dibujar_vidas_corazones(pantalla, player['vidas'], VIDAS_MAXIMAS, heart_surface_local, COLOR_CORAZON_PERDIDO) # Pasar VIDAS_MAXIMAS
        
        # Mostrar el estado del dash cooldown
        if player['dash_cooldown_timer'] > 0:
            tiempo_restante_dash = math.ceil(player['dash_cooldown_timer'] / fps)
            draw_text(pantalla, f"Dash CD: {tiempo_restante_dash}s", ANCHO_PANTALLA - 110, 20, 24, ROJO, "left")
        elif not player['en_dash']:
            draw_text(pantalla, "Dash Listo", ANCHO_PANTALLA - 110, 20, 24, VERDE, "left")

        # Se eliminó la duplicación de dibujar_powerups y la list comprehension aquí.
        
        pygame.display.flip() # Actualizar toda la pantalla
        
        reloj.tick(fps) # Controlar los FPS del juego

    #Lectura de archivo config temporal
    with open(os.path.join(BASE_DIR, "config.json"), "r", encoding="utf-8") as file: # Usar os.path.join para la ruta
        config = json.load(file)

    puntos, nombre = show_game_over(pantalla, config["screen"], config["font_size"], config["colors"], player)

    return puntos, nombre
