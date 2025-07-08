import pygame

def init_player(screen_height: int, player_config: dict) -> dict:
    """
    Inicializa los datos del jugador como un diccionario para un juego horizontal.
    El jugador se posiciona en el lado izquierdo, centrado verticalmente.
    Ahora incluye propiedades para la animación.
    """
    return {
        'rect': pygame.Rect(50, screen_height // 2 - player_config["frame_height"] // 2, player_config["frame_width"], player_config["frame_height"]), # Posición inicial en la izquierda
        'velocidad': player_config["speed"],
        'vidas': player_config["base_health"],
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

def move_player(player_data: dict, keys: pygame.key.ScancodeWrapper, screen_height: int, player_config: dict) -> None:
    """
    Mueve el jugador verticalmente en la pantalla, restringido a los límites verticales.
    Actualiza la dirección para la animación.
    """
    actual_speed = player_data['velocidad']
    if player_data['en_dash']:
        actual_speed *= player_config["dash_velocity_multiplier"]

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

def shoot_player(player_data: dict, current_time: int, bullet_image: pygame.Surface, player_config: dict) -> dict | None:
    """
    Crea un nuevo disparo si el cooldown lo permite.
    Los disparos salen del centro derecho del jugador y se mueven horizontalmente.
    """
    if current_time - player_data['ultima_vez_disparo'] > player_data['cooldown_disparo']:
        player_data['ultima_vez_disparo'] = current_time
        # El disparo sale del lado derecho del jugador
        return {
            'rect': bullet_image.get_rect(midleft=(player_data['rect'].right, player_data['rect'].centery)),
            'velocidad': player_config["shoot_speed"],
            'imagen': bullet_image
        }
    
    return None

def move_shoots(shoots_list: list) -> None:
    """
    Mueve todos los disparos del jugador horizontalmente hacia la derecha.
    """
    for shoot in shoots_list:
        shoot['rect'].x += shoot['velocidad'] # Mover horizontalmente

def use_player_dash(player_data: dict, player_config: dict) -> None:
    """
    Activa el dash del jugador si no está en cooldown.
    """
    if not player_data['en_dash'] and player_data['dash_cooldown_timer'] <= 0:
        player_data['en_dash'] = True
        player_data['dash_timer'] = player_config["dash_duration_ms"]
        player_data['dash_cooldown_timer'] = player_config["dash_cooldown_ms"]

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

def draw_player(screen: pygame.Surface, player_data: dict, player_spritesheet: pygame.Surface, player_config: dict, color_white: tuple) -> None:
    """
    Dibuja el jugador en la pantalla, usando su animación según la dirección.
    Cuando está inactivo ('idle'), muestra un frame estático.
    """
    # Determinar la fila de la animación basada en la dirección
    frame_y = 0 # Valor por defecto, se sobrescribirá
    
    if player_data['direction'] == 'down':
        frame_y = player_config["animation_row_down"] * player_config["frame_height"]
        # 1. Actualizar el temporizador de animación (solo si se está moviendo)
        player_data['animation_timer'] += 1
        if player_data['animation_timer'] >= player_config["animation_speed_fps"]:
            player_data['animation_timer'] = 0
            # 2. Avanzar al siguiente frame
            player_data['current_frame'] = (player_data['current_frame'] + 1) % player_config["total_frames_per_row"]
    elif player_data['direction'] == 'up':
        frame_y = player_config["animation_row_up"] * player_config["frame_height"]
        # 1. Actualizar el temporizador de animación (solo si se está moviendo)
        player_data['animation_timer'] += 1
        if player_data['animation_timer'] >= player_config["animation_speed_fps"]:
            player_data['animation_timer'] = 0
            # 2. Avanzar al siguiente frame
            player_data['current_frame'] = (player_data['current_frame'] + 1) % player_config["total_frames_per_row"]
    elif player_data['direction'] == 'idle':
        frame_y = 85
        player_data['current_frame'] = 0 # Fija el frame en 0 para la animación estática de idle
        player_data['animation_timer'] = 0 # Reinicia el temporizador para que no afecte al volver a moverse


    # 4. Calcular el área del frame actual en la spritesheet
    frame_x = player_data['current_frame'] * player_config["frame_width"]
    frame_rect = pygame.Rect(frame_x, frame_y, player_config["frame_width"], player_config["frame_height"])
    
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