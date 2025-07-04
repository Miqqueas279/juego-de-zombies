import pygame

BASE_HEALTH = 3
BASE_SPEED_PLAYER = 5
BASE_SPEED_SHOOT = 10

# Constantes del Dash del Jugador
DASH_COOLDOWN_FRAMES = 180 # 3 segundos a 60 FPS
DASH_DURATION_FRAMES = 15  # Duración del dash en frames
DASH_VELOCIDAD_MULTIPLIER = 2.5 # Multiplicador de velocidad durante el dash

# --- Constantes de Animación para el Jugador ---
# Asegúrate de que estos valores coincidan con tu spritesheet 'player.png'
PLAYER_FRAME_WIDTH = 40 # Ancho de un solo frame en la spritesheet (sugerido por tus imágenes)
PLAYER_FRAME_HEIGHT = 40 # Alto de un solo frame en la spritesheet (sugerido por tus imágenes)
PLAYER_TOTAL_FRAMES_PER_ROW = 3 # Número total de frames en una fila de animación (parece 3 para caminata)
PLAYER_ANIMATION_SPEED_FPS = 5 # Cuántos frames del juego antes de cambiar al siguiente frame de animación

# Filas de la spritesheet para cada dirección (basado en player.png)
# Asumiendo que la primera fila es índice 0, la segunda 1, etc.
PLAYER_ANIM_ROW_DOWN = 0 # Primera fila para movimiento hacia abajo
PLAYER_ANIM_ROW_UP = 3 # Última fila para movimiento hacia arriba (índice 3 si hay 4 filas)
PLAYER_ANIM_ROW_IDLE = 2 # Fila para inactividad, mirando hacia la derecha (índice 2)

def init_player(scree_height: int) -> dict:
    """
    Inicializa los datos del jugador como un diccionario para un juego horizontal.
    El jugador se posiciona en el lado izquierdo, centrado verticalmente.
    Ahora incluye propiedades para la animación.
    """
    player_width = PLAYER_FRAME_WIDTH # Usamos el tamaño del frame para el rectángulo de colisión
    player_height = PLAYER_FRAME_HEIGHT

    return {
        'rect': pygame.Rect(50, scree_height // 2 - player_height // 2, player_width, player_height), # Posición inicial en la izquierda
        'velocidad': BASE_SPEED_PLAYER,
        'vidas': BASE_HEALTH,
        'puntos': 0,
        'ultima_vez_disparo': 0, # Tiempo en frames desde el último disparo
        'cooldown_disparo': 20, # Frames a esperar entre disparos
        'en_dash': False,
        'dash_timer': 0,
        'dash_cooldown_timer': 0,
        'current_frame': 0, # Frame actual de la animación
        'animation_timer': 0, # Temporizador para controlar la velocidad de la animación
        'direction': 'idle' # Dirección inicial para la animación: 'idle' (mirando al costado)
    }

def move_player(player_data: dict, keys: pygame.key.ScancodeWrapper, screen_height: int) -> None:
    """
    Mueve el jugador verticalmente en la pantalla, restringido a los límites verticales.
    Actualiza la dirección para la animación.
    """
    actual_speed = player_data['velocidad']
    if player_data['en_dash']:
        actual_speed *= DASH_VELOCIDAD_MULTIPLIER

    moving = False
    if keys[pygame.K_UP]:
        player_data['rect'].y -= actual_speed
        player_data['direction'] = 'up' # Establecer dirección para animación
        moving = True
    if keys[pygame.K_DOWN]:
        player_data['rect'].y += actual_speed
        player_data['direction'] = 'down' # Establecer dirección para animación
        moving = True

    # Si no se está moviendo, establecer la dirección 'idle'
    if not moving:
        player_data['direction'] = 'idle' 

    # Restringir al jugador a los límites de la pantalla verticalmente
    if player_data['rect'].top < 0:
        player_data['rect'].top = 0
    if player_data['rect'].bottom > screen_height:
        player_data['rect'].bottom = screen_height

def shoot_player(player_data: dict, current_time: int, bullet_image: pygame.Surface) -> dict | None:
    """
    Crea un nuevo disparo si el cooldown lo permite.
    Los disparos salen del centro derecho del jugador y se mueven horizontalmente.
    """
    if current_time - player_data['ultima_vez_disparo'] > player_data['cooldown_disparo']:
        player_data['ultima_vez_disparo'] = current_time
        # El disparo sale del lado derecho del jugador
        return {
            'rect': bullet_image.get_rect(midleft=(player_data['rect'].right, player_data['rect'].centery)),
            'velocidad': BASE_SPEED_SHOOT,
            'imagen': bullet_image
        }
    
    return None

def move_shoots(shoots_list: list) -> None:
    """
    Mueve todos los disparos del jugador horizontalmente hacia la derecha.
    """
    for shoot in shoots_list:
        shoot['rect'].x += shoot['velocidad'] # Mover horizontalmente

def use_player_dash(player_data: dict) -> None:
    """
    Activa el dash del jugador si no está en cooldown.
    """
    if not player_data['en_dash'] and player_data['dash_cooldown_timer'] <= 0:
        player_data['en_dash'] = True
        player_data['dash_timer'] = DASH_DURATION_FRAMES
        player_data['dash_cooldown_timer'] = DASH_COOLDOWN_FRAMES

def update_player_dash(player_data: dict) -> None:
    """
    Actualiza el temporizador del dash y el cooldown.
    """
    if player_data['en_dash']:
        player_data['dash_timer'] -= 1
        if player_data['dash_timer'] <= 0:
            player_data['en_dash'] = False
    
    if player_data['dash_cooldown_timer'] > 0:
        player_data['dash_cooldown_timer'] -= 1

def draw_player(screen: pygame.Surface, player_data: dict, player_spritesheet: pygame.Surface, color_white: tuple) -> None:
    """
    Dibuja el jugador en la pantalla, usando su animación según la dirección.
    Cuando está inactivo ('idle'), muestra un frame estático.
    """
    # Determinar la fila de la animación basada en la dirección
    frame_y = 0 # Valor por defecto, se sobrescribirá
    
    if player_data['direction'] == 'down':
        frame_y = PLAYER_ANIM_ROW_DOWN * PLAYER_FRAME_HEIGHT
        # 1. Actualizar el temporizador de animación (solo si se está moviendo)
        player_data['animation_timer'] += 1
        if player_data['animation_timer'] >= PLAYER_ANIMATION_SPEED_FPS:
            player_data['animation_timer'] = 0
            # 2. Avanzar al siguiente frame
            player_data['current_frame'] = (player_data['current_frame'] + 1) % PLAYER_TOTAL_FRAMES_PER_ROW
    elif player_data['direction'] == 'up':
        frame_y = PLAYER_ANIM_ROW_UP * PLAYER_FRAME_HEIGHT
        # 1. Actualizar el temporizador de animación (solo si se está moviendo)
        player_data['animation_timer'] += 1
        if player_data['animation_timer'] >= PLAYER_ANIMATION_SPEED_FPS:
            player_data['animation_timer'] = 0
            # 2. Avanzar al siguiente frame
            player_data['current_frame'] = (player_data['current_frame'] + 1) % PLAYER_TOTAL_FRAMES_PER_ROW
    elif player_data['direction'] == 'idle':
        frame_y = 85
        player_data['current_frame'] = 0 # Fija el frame en 0 para la animación estática de idle
        player_data['animation_timer'] = 0 # Reinicia el temporizador para que no afecte al volver a moverse


    # 4. Calcular el área del frame actual en la spritesheet
    frame_x = player_data['current_frame'] * PLAYER_FRAME_WIDTH
    frame_rect = pygame.Rect(frame_x, frame_y, PLAYER_FRAME_WIDTH, PLAYER_FRAME_HEIGHT)
    
    # 5. Extraer el frame actual de la spritesheet
    current_frame_image = player_spritesheet.subsurface(frame_rect)

    # Escalar la imagen del frame para que coincida con el tamaño del rect del jugador (si es necesario)
    scaled_frame_image = pygame.transform.scale(current_frame_image, (player_data['rect'].width, player_data['rect'].height))

    # 6. Dibujar el frame actual en la posición del jugador
    screen.blit(scaled_frame_image, player_data['rect'])

    if player_data['en_dash']:
        pygame.draw.rect(screen, color_white, player_data['rect'].inflate(10, 10), 2, border_radius=5)

def draw_shoots(screen: pygame.Surface, shoots_list: list) -> None:
    """
    Dibuja todos los disparos del jugador en la pantalla.
    """
    for shoot in shoots_list:
        screen.blit(shoot['imagen'], shoot['rect'])