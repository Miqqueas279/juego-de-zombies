import pygame
import random
import math
import os

# Importar funciones auxiliares desde utils.score y utils.text
from utils.score import detectar_colision_rect 
from utils.text import draw_text, get_font

# --- Constantes del Juego ---
COLOR_DISPARO_JUGADOR = (0, 255, 0) # Green (shots are still drawn as colored rectangles)
COLOR_CORAZON_PERDIDO = (50, 50, 50, 150) # Semi-transparent dark gray (with transparency)

VELOCIDAD_JUGADOR_BASE = 5
VELOCIDAD_DISPARO_JUGADOR = 10
VELOCIDAD_ENEMIGO_BASE = 2

VIDAS_INICIALES = 3

# Enemy generation frequency
COOLDOWN_GENERACION_ENEMIGO_FRAMES = 60 # Approximately 1 enemy per second at 60 FPS
# Probabilities of enemy types
PROBABILIDAD_BOOSTED = 0.2 # 20% probability of boosted enemy
PROBABILIDAD_KAMIKAZE = 0.1 # 10% probability of kamikaze
# Speed multipliers for special enemies
FACTOR_VELOCIDAD_BOOSTED = -1.5 # Boosted enemies are 50% lower
FACTOR_VELOCIDAD_KAMIKAZE = 3.0 # Kamikazes are 200% faster
VIDA_KAMIKAZE = 1 # Kamikazes have low health
# Points awarded by enemies
PUNTAJE_NORMAL = 10
PUNTAJE_BOOSTED = 15
PUNTAJE_KAMIKAZE = 25

# Player Dash Constants
DASH_COOLDOWN_FRAMES = 180 # 3 seconds at 60 FPS
DASH_DURATION_FRAMES = 15  # Dash duration in frames
DASH_VELOCIDAD_MULTIPLIER = 2.5 # Speed multiplier during dash

# Resource paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SPRITESHEET_ICONS_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'icons.png') 
FONDO_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'floor.jpg')
PLAYER_IMAGE_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'player.png')
ENEMY_SPRITESHEET_PATH = os.path.join(BASE_DIR, 'assets', 'image', 'ZombieSheet.png')

# Paths for new sounds
SOUND_IMPACT_PATH = os.path.join(BASE_DIR, 'assets', 'sounds', 'impact.mp3')
SOUND_ENEMY_IMPACT_PATH = os.path.join(BASE_DIR, 'assets', 'sounds', 'enemy_impact.mp3')

# --- Zombie Animation Constants ---

ZOMBIE_FRAME_ANCHO = 32  # Ancho de cada frame en la spritesheet original
ZOMBIE_FRAME_ALTO = 32 # Alto de cada frame en la spritesheet original
ZOMBIE_ANIMATION_SPEED = 8 
# Número de frames en la animación de caminar (9 frames por fila en tu spritesheet).
NUM_ZOMBIE_WALK_FRAMES = 9 

ZOMBIE_ANIMATION_ROW = 1 # Fila de animación actual (para el primer zombie, caminar a la izquierda)

# --- Funciones de Manejo de Entidades ---

def init_player(ANCHO_PANTALLA, ALTO_PANTALLA):
    """
    Initializes player data as a dictionary for horizontal gameplay.
    Player starts on the left, moving vertically.
    """
    player_ancho = 50
    player_alto = 50
    return {
        'rect': pygame.Rect(50, ALTO_PANTALLA // 2 - player_alto // 2, player_ancho, player_alto), # Starts on the left, vertically centered
        'velocidad': VELOCIDAD_JUGADOR_BASE,
        'vidas': VIDAS_INICIALES,
        'puntos': 0,
        'ultima_vez_disparo': 0, # Time in frames since last shot
        'cooldown_disparo': 20, # Frames to wait between shots
        'en_dash': False,
        'dash_timer': 0,
        'dash_cooldown_timer': 0
    }

def mover_jugador(player_data, keys, ALTO_PANTALLA): # Now depends on ALTO_PANTALLA
    """
    Updates player position based on pressed keys for vertical movement.
    """
    current_speed = player_data['velocidad']
    if player_data['en_dash']:
        current_speed *= DASH_VELOCIDAD_MULTIPLIER

    if keys[pygame.K_UP]:
        player_data['rect'].y -= current_speed
    if keys[pygame.K_DOWN]:
        player_data['rect'].y += current_speed

    # Limit movement within the screen (now vertically)
    if player_data['rect'].top < 0:
        player_data['rect'].top = 0
    if player_data['rect'].bottom > ALTO_PANTALLA:
        player_data['rect'].bottom = ALTO_PANTALLA

def disparar_jugador(player_data, current_frames):
    """
    Creates a new shot dictionary if cooldown allows (shots to the right).
    """
    if current_frames - player_data['ultima_vez_disparo'] > player_data['cooldown_disparo']:
        player_data['ultima_vez_disparo'] = current_frames
        bullet_ancho = 15 # Horizontal shot, thus wider than tall
        bullet_alto = 5
        return {
            'rect': pygame.Rect(player_data['rect'].right, player_data['rect'].centery - bullet_alto // 2, bullet_ancho, bullet_alto), # Exits from the right of the player
            'velocidad': VELOCIDAD_DISPARO_JUGADOR,
            'color': COLOR_DISPARO_JUGADOR,
            'origen': 'jugador'
        }
    return None

def usar_dash_jugador(player_data):
    """
    Activates dash for the player if cooldown allows.
    """
    if player_data['dash_cooldown_timer'] <= 0:
        player_data['en_dash'] = True
        player_data['dash_timer'] = DASH_DURATION_FRAMES
        player_data['dash_cooldown_timer'] = DASH_COOLDOWN_FRAMES
        return True
    return False

def actualizar_dash_jugador(player_data):
    """
    Updates dash status and its timer.
    """
    if player_data['en_dash']:
        player_data['dash_timer'] -= 1
        if player_data['dash_timer'] <= 0:
            player_data['en_dash'] = False
    
    if player_data['dash_cooldown_timer'] > 0:
        player_data['dash_cooldown_timer'] -= 1

def dibujar_jugador(pantalla, player_data, player_image): 
    """
    Draws the player on the screen.
    """
    pantalla.blit(player_image, player_data['rect'])

    # White border for dash remains
    if player_data['en_dash']:
        pygame.draw.rect(pantalla, (255, 255, 255), player_data['rect'].inflate(10, 10), 2, border_radius=5)


def generar_enemigo(ALTO_PANTALLA): # Now depends on ALTO_PANTALLA
    """
    Creates a new enemy dictionary with random properties for horizontal gameplay.
    Enemies appear from the right, moving horizontally.
    """
    enemy_ancho = 40
    enemy_alto = 40
    # Random Y position on the right side
    y_pos = random.randint(enemy_alto // 2, ALTO_PANTALLA - enemy_alto // 2)
    x_pos = 800 + enemy_ancho # Starts just off-screen to the right (ANCHO_PANTALLA + enemy_ancho)

    # Base properties
    velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE
    vida_enemigo = 1
    puntaje_enemigo = PUNTAJE_NORMAL
    tipo_enemigo = "normal"

    # Determine special enemy type
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
        'puntos': puntaje_enemigo,
        'animation_frame': 0, # Index of the current animation frame
        'frame_update_counter': 0 # Counter to control animation speed
    }

def mover_enemigos(enemigos_list):
    """
    Updates the position of all enemies in the list (leftward movement).
    """
    for enemigo in enemigos_list:
        enemigo['rect'].x -= enemigo['velocidad']
        # Update animation frame
        enemigo['frame_update_counter'] += 1
        if enemigo['frame_update_counter'] >= ZOMBIE_ANIMATION_SPEED:
            enemigo['animation_frame'] = (enemigo['animation_frame'] + 1) % NUM_ZOMBIE_WALK_FRAMES
            enemigo['frame_update_counter'] = 0

def dibujar_enemigos(pantalla, enemigos_list, enemy_spritesheet, zombie_walk_frames): # zombie_walk_frames is now passed
    """
    Draws all enemies on the screen using the current frame of their animation.
    """
    for enemigo in enemigos_list:
        current_frame_rect = zombie_walk_frames[enemigo['animation_frame']]
        pantalla.blit(enemy_spritesheet, enemigo['rect'], current_frame_rect)

def mover_disparos(disparos_list):
    """
    Updates the position of all shots in the list (rightward movement).
    """
    for disparo in disparos_list:
        disparo['rect'].x += disparo['velocidad']

def dibujar_disparos(pantalla, disparos_list):
    """
    Draws all shots on the screen.
    """
    for disparo in disparos_list:
        pygame.draw.rect(pantalla, disparo['color'], disparo['rect'])

def limpiar_entidades_fuera_pantalla(enemigos_list, disparos_list, ANCHO_PANTALLA):
    """
    Removes enemies and shots that have left the screen (horizontal limits).
    """
    # Clear enemies (have left on the left side)
    i = len(enemigos_list) - 1
    while i >= 0:
        if enemigos_list[i]['rect'].right < 0:
            del enemigos_list[i]
        i -= 1
    
    # Clear shots (have left on the right side)
    i = len(disparos_list) - 1
    while i >= 0:
        if disparos_list[i]['rect'].left > ANCHO_PANTALLA:
            del disparos_list[i]
        i -= 1

def manejar_colisiones(player_data, enemigos_list, player_bullets_list, player_impact_sound, enemy_impact_sound): # Sound parameters added
    """
    Handles all collisions between entities and updates lives/points.
    Returns True if the game ends (player's lives <= 0), False otherwise.
    """
    game_over = False

    # Player shots collision with enemies
    i_bullet = len(player_bullets_list) - 1
    while i_bullet >= 0:
        bullet = player_bullets_list[i_bullet]
        j_enemy = len(enemigos_list) - 1
        bullet_hit = False # Flag to know if the bullet hit
        while j_enemy >= 0:
            enemy = enemigos_list[j_enemy]
            if detectar_colision_rect(bullet['rect'], enemy['rect']):
                enemy['vida'] -= 1
                enemy_impact_sound.play() # Play sound
                bullet_hit = True # Bullet hit, must be removed
                if enemy['vida'] <= 0:
                    player_data['puntos'] += enemy['puntos'] # Add points for destroyed enemy
                    del enemigos_list[j_enemy] # Remove enemy
                break # Exit inner loop, shot already hit
            j_enemy -= 1
        
        if bullet_hit:
            del player_bullets_list[i_bullet] # Remove the shot
        i_bullet -= 1

    # Enemy collision with player
    i_enemy = len(enemigos_list) - 1
    while i_enemy >= 0:
        enemy = enemigos_list[i_enemy]
        if detectar_colision_rect(player_data['rect'], enemy['rect']):
            player_data['vidas'] -= 1
            player_impact_sound.play() # Play sound
            del enemigos_list[i_enemy] # Enemy is destroyed upon hitting the player
            if player_data['vidas'] <= 0:
                game_over = True # Game over
                break # No need to continue checking enemies
        i_enemy -= 1
    
    return game_over

def dibujar_vidas_corazones(pantalla, vidas_actuales, vidas_maximas, heart_image_surface, lost_heart_color):
    """
    Draws life hearts in Minecraft style.
    """
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


# --- Main Game Loop (main_game_loop) ---
def main_game_loop(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_pequena, NEGRO, BLANCO, ROJO, VERDE, AZUL):
    """
    Manages the main game logic in horizontal mode with zombie animation.
    Returns the final score and player name if the game ends.
    """
    # Load resources once when the game loop starts
    if not hasattr(main_game_loop, 'resources_cached'):
        main_game_loop.resources_cached = {}
        
        # Load background
        main_game_loop.resources_cached['fondo_surface'] = pygame.image.load(FONDO_PATH).convert()
        main_game_loop.resources_cached['fondo_surface'] = pygame.transform.scale(
            main_game_loop.resources_cached['fondo_surface'], (ANCHO_PANTALLA, ALTO_PANTALLA)
        )

        # Load player image and enemy spritesheet
        main_game_loop.resources_cached['player_image'] = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        main_game_loop.resources_cached['enemy_spritesheet'] = pygame.image.load(ENEMY_SPRITESHEET_PATH).convert_alpha() # Carga la spritesheet completa

        # Scale images (only player, enemy is scaled when drawing each frame)
        main_game_loop.resources_cached['player_image'] = pygame.transform.scale(
            main_game_loop.resources_cached['player_image'], (50, 50)
        )
        
        # Calculate scale factor for zombie frames to be 40x40
        # This is important if your collision rect size (40x40)
        # does not match the original frame size in the spritesheet (32x32).
        scale_factor_x = 40 / ZOMBIE_FRAME_ANCHO
        scale_factor_y = 40 / ZOMBIE_FRAME_ALTO
        
        # Scale the entire zombie spritesheet once here
        main_game_loop.resources_cached['enemy_spritesheet'] = pygame.transform.scale(
            main_game_loop.resources_cached['enemy_spritesheet'], 
            (int(main_game_loop.resources_cached['enemy_spritesheet'].get_width() * scale_factor_x), 
             int(main_game_loop.resources_cached['enemy_spritesheet'].get_height() * scale_factor_y))
        )
        
        # Calculate and store the scaled animation frame rectangles
        # This is the list that 'draw_enemies' will use to know which part of the spritesheet to draw.
        scaled_zombie_walk_frames = []
        for i in range(NUM_ZOMBIE_WALK_FRAMES):
            # Calculate the X and Y coordinates of the original frame in the spritesheet.
            frame_x = i * ZOMBIE_FRAME_ANCHO
            # AQUI SE USA ZOMBIE_ANIMATION_ROW PARA SELECCIONAR LA FILA COMPLETA
            frame_y = ZOMBIE_ANIMATION_ROW * ZOMBIE_FRAME_ALTO 
            original_rect = pygame.Rect(frame_x, frame_y, ZOMBIE_FRAME_ANCHO, ZOMBIE_FRAME_ALTO)
            
            # Scale each coordinate and dimension of the rectangle to match the spritesheet's scaling.
            scaled_x = int(original_rect.x * scale_factor_x)
            scaled_y = int(original_rect.y * scale_factor_y)
            scaled_width = int(original_rect.width * scale_factor_x)
            scaled_height = int(original_rect.height * scale_factor_y)
            scaled_zombie_walk_frames.append(pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height))
        
        # Store the scaled frames list in the resource cache
        main_game_loop.resources_cached['zombie_walk_frames'] = scaled_zombie_walk_frames


        # Load icons spritesheet and extract heart
        spritesheet_icons = pygame.image.load(SPRITESHEET_ICONS_PATH).convert_alpha()
        HEART_SPRITE_RECT_SOURCE = pygame.Rect(52, 0, 9, 9) 
        main_game_loop.resources_cached['heart_surface_local'] = spritesheet_icons.subsurface(HEART_SPRITE_RECT_SOURCE)
        
        SCALE_SIZE = (30, 30)
        main_game_loop.resources_cached['heart_surface_local'] = pygame.transform.scale(
            main_game_loop.resources_cached['heart_surface_local'], SCALE_SIZE
        )

        # Load sounds and cache them
        player_impact_sound = pygame.mixer.Sound(SOUND_IMPACT_PATH)
        player_impact_sound.set_volume(0.3)
        main_game_loop.resources_cached['player_impact_sound'] = player_impact_sound

        enemy_impact_sound = pygame.mixer.Sound(SOUND_ENEMY_IMPACT_PATH)
        enemy_impact_sound.set_volume(0.1)
        main_game_loop.resources_cached['enemy_impact_sound'] = enemy_impact_sound


    # Get surfaces and sound instances from cache
    fondo_surface = main_game_loop.resources_cached['fondo_surface']
    player_image = main_game_loop.resources_cached['player_image']
    enemy_spritesheet = main_game_loop.resources_cached['enemy_spritesheet'] 
    zombie_walk_frames = main_game_loop.resources_cached['zombie_walk_frames'] # Get frames from cache
    heart_surface_to_use = main_game_loop.resources_cached['heart_surface_local']
    player_impact_sound = main_game_loop.resources_cached['player_impact_sound']
    enemy_impact_sound = main_game_loop.resources_cached['enemy_impact_sound']

    reloj = pygame.time.Clock()
    fps = 60

    # Initialize player data
    player = init_player(ANCHO_PANTALLA, ALTO_PANTALLA)
    
    # Lists to store enemies and shots
    enemigos = []
    player_bullets = []

    frames_desde_ultima_generacion_enemigo = 0 # Counter for enemy generation

    running = True
    while running:
        current_frames = pygame.time.get_ticks() // (1000 // fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None, None
            if event.type == pygame.KEYDOWN: # Check for KEYDOWN event
                if event.key == pygame.K_SPACE:
                    nuevo_disparo = disparar_jugador(player, current_frames)
                    if nuevo_disparo:
                        player_bullets.append(nuevo_disparo)
                if event.key == pygame.K_z: # Key for dash
                    usar_dash_jugador(player)

        # --- Player Movement ---
        keys = pygame.key.get_pressed()
        mover_jugador(player, keys, ALTO_PANTALLA)
        actualizar_dash_jugador(player)

        # --- Enemy Generation ---
        frames_desde_ultima_generacion_enemigo += 1
        if frames_desde_ultima_generacion_enemigo >= COOLDOWN_GENERACION_ENEMIGO_FRAMES:
            enemigos.append(generar_enemigo(ALTO_PANTALLA))
            frames_desde_ultima_generacion_enemigo = 0

        # --- Enemy and Shot Movement ---
        mover_enemigos(enemigos) # This function now also updates the zombie animation frame
        mover_disparos(player_bullets)

        # --- Collisions ---
        game_over = manejar_colisiones(player, enemigos, player_bullets, player_impact_sound, enemy_impact_sound)
        if game_over:
            running = False

        # --- Clear off-screen entities ---
        limpiar_entidades_fuera_pantalla(enemigos, player_bullets, ANCHO_PANTALLA)

        # --- Draw ---
        pantalla.blit(fondo_surface, (0, 0))

        dibujar_jugador(pantalla, player, player_image) 
        # Here the full spritesheet AND the scaled frames list are passed.
        dibujar_enemigos(pantalla, enemigos, enemy_spritesheet, zombie_walk_frames) 
        dibujar_disparos(pantalla, player_bullets) 

        # Draw UI (lives and score)
        draw_text(pantalla, f"Puntaje: {player['puntos']}", 15, 20, 24, BLANCO, "left", font=fuente_pequena)
        dibujar_vidas_corazones(pantalla, player['vidas'], VIDAS_INICIALES, heart_surface_to_use, COLOR_CORAZON_PERDIDO)
        
        # Show dash cooldown status
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
