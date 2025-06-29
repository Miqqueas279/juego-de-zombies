import pygame
import random
import math
import os

# Importar funciones auxiliares desde utils.score y utils.text
from utils.score import detectar_colision_rect 
from utils.text import draw_text, get_font

# --- Constantes del Juego ---
COLOR_DISPARO_JUGADOR = (0, 255, 0) # Verde (los disparos aún se dibujan como rectángulos de color)
COLOR_CORAZON_PERDIDO = (50, 50, 50, 150) # Gris oscuro semi-transparente (con transparencia)

VELOCIDAD_JUGADOR_BASE = 5
VELOCIDAD_DISPARO_JUGADOR = 10
VELOCIDAD_ENEMIGO_BASE = 2

VIDAS_INICIALES = 3

# Frecuencia de generación de enemigos
COOLDOWN_GENERACION_ENEMIGO_FRAMES = 60 # Aproximadamente 1 enemigo por segundo a 60 FPS
# Probabilidades de tipos de enemigos
PROBABILIDAD_BOOSTED = 0.2 # 20% de probabilidad de enemigo con boost
PROBABILIDAD_KAMIKAZE = 0.1 # 10% de probabilidad de kamikaze
# Multiplicadores de velocidad para enemigos especiales
FACTOR_VELOCIDAD_BOOSTED = 1.5 # Los enemigos con boost son 50% más rápidos
FACTOR_VELOCIDAD_KAMIKAZE = 3.0 # Los kamikazes son 200% más rápidos
VIDA_KAMIKAZE = 1 # Los kamikazes tienen poca vida
# Puntos que otorgan los enemigos
PUNTAJE_NORMAL = 10
PUNTAJE_BOOSTED = 15
PUNTAJE_KAMIKAZE = 25

# Constantes del Dash del Jugador
DASH_COOLDOWN_FRAMES = 180 # 3 segundos a 60 FPS
DASH_DURATION_FRAMES = 15  # Duración del dash en frames
DASH_VELOCIDAD_MULTIPLIER = 2.5 # Multiplicador de velocidad durante el dash

# Rutas de recursos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SPRITESHEET_ICONS_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'icons.png') 
FONDO_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'floor.jpg')
PLAYER_IMAGE_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'player.png')
ENEMY_IMAGE_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'zombie.png')

# Rutas para los nuevos sonidos
SOUND_IMPACT_PATH = os.path.join(BASE_DIR, 'assets', 'sounds', 'impact.mp3')
SOUND_ENEMY_IMPACT_PATH = os.path.join(BASE_DIR, 'assets', 'sounds', 'enemy_impact.mp3')


# --- Funciones de Manejo de Entidades ---

def init_player(ANCHO_PANTALLA, ALTO_PANTALLA):
    """
    Inicializa los datos del jugador como un diccionario para juego horizontal.
    El jugador inicia a la izquierda, moviéndose verticalmente.
    """
    player_ancho = 50
    player_alto = 50
    return {
        'rect': pygame.Rect(50, ALTO_PANTALLA // 2 - player_alto // 2, player_ancho, player_alto), # Inicia a la izquierda, centrado verticalmente
        'velocidad': VELOCIDAD_JUGADOR_BASE,
        'vidas': VIDAS_INICIALES,
        'puntos': 0,
        'ultima_vez_disparo': 0, # Tiempo en frames desde el último disparo
        'cooldown_disparo': 20, # Frames a esperar entre disparos
        'en_dash': False,
        'dash_timer': 0,
        'dash_cooldown_timer': 0
    }

def mover_jugador(player_data, keys, ALTO_PANTALLA): # Ahora depende de ALTO_PANTALLA
    """
    Actualiza la posición del jugador según las teclas presionadas para movimiento vertical.
    """
    current_speed = player_data['velocidad']
    if player_data['en_dash']:
        current_speed *= DASH_VELOCIDAD_MULTIPLIER

    if keys[pygame.K_UP]:
        player_data['rect'].y -= current_speed
    if keys[pygame.K_DOWN]:
        player_data['rect'].y += current_speed

    # Limitar el movimiento dentro de la pantalla (ahora verticalmente)
    if player_data['rect'].top < 0:
        player_data['rect'].top = 0
    if player_data['rect'].bottom > ALTO_PANTALLA:
        player_data['rect'].bottom = ALTO_PANTALLA

def disparar_jugador(player_data, current_frames):
    """
    Crea un nuevo diccionario de disparo si el cooldown lo permite (disparos hacia la derecha).
    """
    if current_frames - player_data['ultima_vez_disparo'] > player_data['cooldown_disparo']:
        player_data['ultima_vez_disparo'] = current_frames
        bullet_ancho = 15 # Disparo horizontal, por lo tanto más ancho que alto
        bullet_alto = 5
        return {
            'rect': pygame.Rect(player_data['rect'].right, player_data['rect'].centery - bullet_alto // 2, bullet_ancho, bullet_alto), # Sale de la derecha del jugador
            'velocidad': VELOCIDAD_DISPARO_JUGADOR,
            'color': COLOR_DISPARO_JUGADOR,
            'origen': 'jugador'
        }
    return None

def usar_dash_jugador(player_data):
    """
    Activa el dash para el jugador si el cooldown lo permite.
    """
    if player_data['dash_cooldown_timer'] <= 0:
        player_data['en_dash'] = True
        player_data['dash_timer'] = DASH_DURATION_FRAMES
        player_data['dash_cooldown_timer'] = DASH_COOLDOWN_FRAMES
        return True
    return False

def actualizar_dash_jugador(player_data):
    """
    Actualiza el estado del dash y su temporizador.
    """
    if player_data['en_dash']:
        player_data['dash_timer'] -= 1
        if player_data['dash_timer'] <= 0:
            player_data['en_dash'] = False
    
    if player_data['dash_cooldown_timer'] > 0:
        player_data['dash_cooldown_timer'] -= 1

def dibujar_jugador(pantalla, player_data, player_image): 
    """
    Dibuja el jugador en la pantalla.
    """
    pantalla.blit(player_image, player_data['rect'])

    # El borde blanco para el dash se mantiene
    if player_data['en_dash']:
        pygame.draw.rect(pantalla, (255, 255, 255), player_data['rect'].inflate(10, 10), 2, border_radius=5)


def generar_enemigo(ALTO_PANTALLA): # Ahora depende de ALTO_PANTALLA
    """
    Crea un nuevo diccionario de enemigo con propiedades aleatorias para juego horizontal.
    Los enemigos aparecen a la derecha, moviéndose horizontalmente.
    """
    enemy_ancho = 40
    enemy_alto = 40
    # Posición Y aleatoria en la parte derecha
    y_pos = random.randint(enemy_alto // 2, ALTO_PANTALLA - enemy_alto // 2)
    x_pos = 800 + enemy_ancho # Empieza justo fuera de la pantalla por la derecha (ANCHO_PANTALLA + enemy_ancho)

    # Propiedades base
    velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE
    vida_enemigo = 1
    puntaje_enemigo = PUNTAJE_NORMAL
    tipo_enemigo = "normal"

    # Determinar tipo de enemigo especial
    r = random.random()
    if r < PROBABILIDAD_KAMIKAZE:
        tipo_enemigo = "kamikaze"
        velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE * FACTOR_VELOCIDAD_KAMIKAZE
        vida_enemigo = VIDA_KAMIKAZE
        puntaje_enemigo = PUNTAJE_KAMIKAZE
    elif r < PROBABILIDAD_KAMIKAZE + PROBABILIDAD_BOOSTED:
        tipo_enemigo = "boosted"
        velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE * FACTOR_VELOCIDAD_BOOSTED
        puntaje_enemigo = PUNTAJE_BOOSTED
    
    return {
        'rect': pygame.Rect(x_pos - enemy_ancho // 2, y_pos - enemy_alto // 2, enemy_ancho, enemy_alto),
        'velocidad': velocidad_enemigo,
        'vida': vida_enemigo,
        'tipo': tipo_enemigo,
        'puntos': puntaje_enemigo
    }

def mover_enemigos(enemigos_list):
    """
    Actualiza la posición de todos los enemigos en la lista (movimiento hacia la izquierda).
    """
    for enemigo in enemigos_list:
        enemigo['rect'].x -= enemigo['velocidad'] # Ahora mueven en X

def dibujar_enemigos(pantalla, enemigos_list, enemy_image): 
    """
    Dibuja todos los enemigos en la pantalla usando su sprite.
    """
    for enemigo in enemigos_list:
        pantalla.blit(enemy_image, enemigo['rect'])

def mover_disparos(disparos_list):
    """
    Actualiza la posición de todos los disparos en la lista (movimiento hacia la derecha).
    """
    for disparo in disparos_list:
        disparo['rect'].x += disparo['velocidad'] # Ahora mueven en X

def dibujar_disparos(pantalla, disparos_list):
    """
    Dibuja todos los disparos en la pantalla.
    """
    for disparo in disparos_list:
        pygame.draw.rect(pantalla, disparo['color'], disparo['rect'])

def limpiar_entidades_fuera_pantalla(enemigos_list, disparos_list, ANCHO_PANTALLA): # Ahora depende de ANCHO_PANTALLA
    """
    Elimina enemigos y disparos que han salido de la pantalla (límites horizontales).
    """
    # Limpiar enemigos (han salido por la izquierda)
    i = len(enemigos_list) - 1
    while i >= 0:
        if enemigos_list[i]['rect'].right < 0: # Si el enemigo ha cruzado el borde izquierdo
            del enemigos_list[i]
        i -= 1
    
    # Limpiar disparos (han salido por la derecha)
    i = len(disparos_list) - 1
    while i >= 0:
        if disparos_list[i]['rect'].left > ANCHO_PANTALLA: # Si el disparo ha cruzado el borde derecho
            del disparos_list[i]
        i -= 1

def manejar_colisiones(player_data, enemigos_list, player_bullets_list, player_impact_sound, enemy_impact_sound):
    """
    Maneja todas las colisiones entre entidades y actualiza vidas/puntos.
    Retorna True si el juego termina (vidas del jugador <= 0), False en caso contrario.
    """
    game_over = False

    # Colisión disparos del jugador con enemigos
    i_bullet = len(player_bullets_list) - 1
    while i_bullet >= 0:
        bullet = player_bullets_list[i_bullet]
        j_enemy = len(enemigos_list) - 1
        bullet_hit = False
        while j_enemy >= 0:
            enemy = enemigos_list[j_enemy]
            if detectar_colision_rect(bullet['rect'], enemy['rect']):
                enemy['vida'] -= 1
                enemy_impact_sound.play()
                bullet_hit = True
                if enemy['vida'] <= 0:
                    player_data['puntos'] += enemy['puntos']
                    del enemigos_list[j_enemy]
                break
            j_enemy -= 1
        
        if bullet_hit:
            del player_bullets_list[i_bullet]
        i_bullet -= 1

    # Colisión enemigo con jugador
    i_enemy = len(enemigos_list) - 1
    while i_enemy >= 0:
        enemy = enemigos_list[i_enemy]
        if detectar_colision_rect(player_data['rect'], enemy['rect']):
            player_data['vidas'] -= 1
            player_impact_sound.play()
            del enemigos_list[i_enemy]
            if player_data['vidas'] <= 0:
                game_over = True
                break
        i_enemy -= 1
    
    return game_over

def dibujar_vidas_corazones(pantalla, vidas_actuales, vidas_maximas, heart_image_surface, lost_heart_color):
    """
    Dibuja los corazones de vida al estilo Minecraft.
    """
    # Cambiamos la posición de los corazones para que estén en la esquina superior derecha o inferior izquierda
    # Los pondré en la esquina superior izquierda como antes, pero ajustando si es necesario.
    x_offset = 10 
    y_offset = 40
    spacing = heart_image_surface.get_width() + 5 

    for i in range(vidas_maximas):
        if i < vidas_actuales:
            pantalla.blit(heart_image_surface, (x_offset + i * spacing, y_offset))
        else:
            lost_heart_rect = pygame.Rect(x_offset + i * spacing, y_offset, 
                                          heart_image_surface.get_width(), 
                                          heart_image_surface.get_height()) 
            s = pygame.Surface(lost_heart_rect.size, pygame.SRCALPHA)
            s.fill(lost_heart_color)
            pantalla.blit(s, lost_heart_rect)


# --- Bucle Principal del Juego (main_game_loop) ---
def main_game_loop(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_pequena, NEGRO, BLANCO, ROJO, VERDE, AZUL):
    """
    Gestiona la lógica principal de la partida en modo horizontal.
    Retorna el puntaje final y el nombre del jugador si el juego termina.
    """
    # Cargar los recursos una única vez al iniciar el bucle del juego
    if not hasattr(main_game_loop, 'resources_cached'):
        main_game_loop.resources_cached = {}
        # Carga directa de todos los recursos (sin try-except)
        # Cargar fondo
        main_game_loop.resources_cached['fondo_surface'] = pygame.image.load(FONDO_PATH).convert()
        main_game_loop.resources_cached['fondo_surface'] = pygame.transform.scale(
            main_game_loop.resources_cached['fondo_surface'], (ANCHO_PANTALLA, ALTO_PANTALLA)
        )

        # Cargar imágenes de jugador y enemigo
        # Podrías querer rotar los sprites si el jugador/enemigos miran hacia un lado.
        # Por ahora, los dejamos en su orientación original.
        main_game_loop.resources_cached['player_image'] = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        main_game_loop.resources_cached['enemy_image'] = pygame.image.load(ENEMY_IMAGE_PATH).convert_alpha()

        # Escalar imágenes al tamaño del rectángulo
        main_game_loop.resources_cached['player_image'] = pygame.transform.scale(
            main_game_loop.resources_cached['player_image'], (50, 50)
        )
        main_game_loop.resources_cached['enemy_image'] = pygame.transform.scale(
            main_game_loop.resources_cached['enemy_image'], (40, 40)
        )

        # Cargar la spritesheet de iconos y extraer el corazón
        spritesheet = pygame.image.load(SPRITESHEET_ICONS_PATH).convert_alpha()
        HEART_SPRITE_RECT_SOURCE = pygame.Rect(52, 0, 9, 9) 
        main_game_loop.resources_cached['heart_surface_local'] = spritesheet.subsurface(HEART_SPRITE_RECT_SOURCE)
        
        SCALE_SIZE = (30, 30)
        main_game_loop.resources_cached['heart_surface_local'] = pygame.transform.scale(
            main_game_loop.resources_cached['heart_surface_local'], SCALE_SIZE
        )

        # Cargar sonidos y almacenarlos en caché
        player_impact_sound = pygame.mixer.Sound(SOUND_IMPACT_PATH)
        player_impact_sound.set_volume(0.3)
        main_game_loop.resources_cached['player_impact_sound'] = player_impact_sound

        enemy_impact_sound = pygame.mixer.Sound(SOUND_ENEMY_IMPACT_PATH)
        enemy_impact_sound.set_volume(0.1)
        main_game_loop.resources_cached['enemy_impact_sound'] = enemy_impact_sound


    # Obtener las superficies e instancias de sonido desde el caché
    fondo_surface = main_game_loop.resources_cached['fondo_surface']
    player_image = main_game_loop.resources_cached['player_image']
    enemy_image = main_game_loop.resources_cached['enemy_image']
    heart_surface_to_use = main_game_loop.resources_cached['heart_surface_local']
    player_impact_sound = main_game_loop.resources_cached['player_impact_sound']
    enemy_impact_sound = main_game_loop.resources_cached['enemy_impact_sound']

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
        current_frames = pygame.time.get_ticks() // (1000 // fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    nuevo_disparo = disparar_jugador(player, current_frames)
                    if nuevo_disparo:
                        player_bullets.append(nuevo_disparo)
                if event.key == pygame.K_z: # Tecla para el dash
                    usar_dash_jugador(player)

        # --- Movimiento del Jugador ---
        keys = pygame.key.get_pressed()
        mover_jugador(player, keys, ALTO_PANTALLA) # Ahora se pasa ALTO_PANTALLA
        actualizar_dash_jugador(player)

        # --- Generación de Enemigos ---
        frames_desde_ultima_generacion_enemigo += 1
        if frames_desde_ultima_generacion_enemigo >= COOLDOWN_GENERACION_ENEMIGO_FRAMES:
            enemigos.append(generar_enemigo(ALTO_PANTALLA)) # Ahora se pasa ALTO_PANTALLA
            frames_desde_ultima_generacion_enemigo = 0

        # --- Movimiento de Enemigos y Disparos ---
        mover_enemigos(enemigos)
        mover_disparos(player_bullets)

        # --- Colisiones ---
        game_over = manejar_colisiones(player, enemigos, player_bullets, player_impact_sound, enemy_impact_sound)
        if game_over:
            running = False

        # --- Eliminar elementos fuera de pantalla ---
        limpiar_entidades_fuera_pantalla(enemigos, player_bullets, ANCHO_PANTALLA) # Ahora se pasa ANCHO_PANTALLA

        # --- Dibujar ---
        pantalla.blit(fondo_surface, (0, 0)) # Dibujar el fondo

        dibujar_jugador(pantalla, player, player_image) 
        dibujar_enemigos(pantalla, enemigos, enemy_image) 
        dibujar_disparos(pantalla, player_bullets) 

        # Dibujar UI (vidas y puntaje)
        draw_text(pantalla, f"Puntaje: {player['puntos']}", 15, 20, 24, BLANCO, "left", font=fuente_pequena)
        dibujar_vidas_corazones(pantalla, player['vidas'], VIDAS_INICIALES, heart_surface_to_use, COLOR_CORAZON_PERDIDO)
        
        # Mostrar el estado del dash cooldown (ajustar posición para layout horizontal)
        # Podríamos moverlo a la esquina inferior derecha o seguir en la superior derecha
        # Lo mantendré en la superior derecha por ahora.
        if player['dash_cooldown_timer'] > 0:
            tiempo_restante_dash = math.ceil(player['dash_cooldown_timer'] / fps)
            draw_text(pantalla, f"Dash CD: {tiempo_restante_dash}s", ANCHO_PANTALLA - 10, 20, 24, ROJO, "right", font=fuente_pequena)
        elif not player['en_dash']:
            draw_text(pantalla, "Dash Listo", ANCHO_PANTALLA - 10, 20, 24, VERDE, "right", font=fuente_pequena)


        pygame.display.flip()

        reloj.tick(fps)

    # --- Game Over Screen ---
    nombre_ingresado = ""
    input_activo = True
    game_over_font_title = get_font(74)
    game_over_font_score = get_font(36)
    game_over_font_input = get_font(36)

    while input_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_activo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre_ingresado = nombre_ingresado[:-1]
                else:
                    nombre_ingresado += event.unicode

        pantalla.fill(NEGRO)
        draw_text(pantalla, "GAME OVER", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 50, 74, ROJO, "center", font=game_over_font_title)
        draw_text(pantalla, f"Puntaje Final: {player['puntos']}", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 20, 36, BLANCO, "center", font=game_over_font_score)
        draw_text(pantalla, "Ingresa tu nombre:", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 80, 36, BLANCO, "center", font=game_over_font_input)
        draw_text(pantalla, nombre_ingresado + "|", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 120, 36, BLANCO, "center", font=game_over_font_input)
        pygame.display.flip()

    return player['puntos'], nombre_ingresado
