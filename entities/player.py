import pygame

GREEN = (0, 255, 0)
VIDAS_INICIALES = 3
VELOCIDAD_JUGADOR_BASE = 5
VELOCIDAD_DISPARO_JUGADOR = 10

# Constantes del Dash del Jugador
DASH_COOLDOWN_FRAMES = 180 # 3 segundos a 60 FPS
DASH_DURATION_FRAMES = 15  # Duración del dash en frames
DASH_VELOCIDAD_MULTIPLIER = 2.5 # Multiplicador de velocidad durante el dash

def init_player(ANCHO_PANTALLA, ALTO_PANTALLA):
    """
    Inicializa los datos del jugador como un diccionario para un juego horizontal.
    El jugador se posiciona en el lado izquierdo, centrado verticalmente.
    """
    player_ancho = 50
    player_alto = 50
    return {
        'rect': pygame.Rect(50, ALTO_PANTALLA // 2 - player_alto // 2, player_ancho, player_alto), # Posición inicial en la izquierda
        'velocidad': VELOCIDAD_JUGADOR_BASE,
        'vidas': VIDAS_INICIALES,
        'puntos': 0,
        'ultima_vez_disparo': 0, # Tiempo en frames desde el último disparo
        'cooldown_disparo': 20, # Frames a esperar entre disparos
        'en_dash': False,
        'dash_timer': 0,
        'dash_cooldown_timer': 0
    }

def mover_jugador(player_data: dict, keys: pygame.key.ScancodeWrapper, ALTO_PANTALLA: int) -> None:
    """
    Mueve el jugador verticalmente en la pantalla, restringido a los límites verticales.
    """
    velocidad_actual = player_data['velocidad']
    if player_data['en_dash']:
        velocidad_actual *= DASH_VELOCIDAD_MULTIPLIER

    # Movimiento vertical
    if keys[pygame.K_UP]:
        player_data['rect'].y -= velocidad_actual
    if keys[pygame.K_DOWN]:
        player_data['rect'].y += velocidad_actual

    # Restringir al jugador a los límites de la pantalla verticalmente
    if player_data['rect'].top < 0:
        player_data['rect'].top = 0
    if player_data['rect'].bottom > ALTO_PANTALLA:
        player_data['rect'].bottom = ALTO_PANTALLA

def disparar_jugador(player_data: dict, current_time: int) -> dict | None:
    """
    Crea un nuevo disparo si el cooldown lo permite.
    Los disparos salen del centro derecho del jugador y se mueven horizontalmente.
    """
    if current_time - player_data['ultima_vez_disparo'] > player_data['cooldown_disparo']:
        player_data['ultima_vez_disparo'] = current_time
        bullet_ancho = 10
        bullet_alto = 5
        # El disparo sale del lado derecho del jugador
        return {
            'rect': pygame.Rect(player_data['rect'].right, player_data['rect'].centery - bullet_alto // 2, bullet_ancho, bullet_alto),
            'velocidad': VELOCIDAD_DISPARO_JUGADOR
        }
    return None

def mover_disparos(disparos_list: list) -> None:
    """
    Mueve todos los disparos del jugador horizontalmente hacia la derecha.
    """
    for disparo in disparos_list:
        disparo['rect'].x += disparo['velocidad'] # Mover horizontalmente

def usar_dash_jugador(player_data: dict) -> None:
    """
    Activa el dash del jugador si no está en cooldown.
    """
    if not player_data['en_dash'] and player_data['dash_cooldown_timer'] <= 0:
        player_data['en_dash'] = True
        player_data['dash_timer'] = DASH_DURATION_FRAMES
        player_data['dash_cooldown_timer'] = DASH_COOLDOWN_FRAMES

def actualizar_dash_jugador(player_data: dict) -> None:
    """
    Actualiza el temporizador del dash y el cooldown.
    """
    if player_data['en_dash']:
        player_data['dash_timer'] -= 1
        if player_data['dash_timer'] <= 0:
            player_data['en_dash'] = False
    
    if player_data['dash_cooldown_timer'] > 0:
        player_data['dash_cooldown_timer'] -= 1

def dibujar_jugador(pantalla: pygame.Surface, player_data: dict, player_image: pygame.Surface, AZUL: tuple, BLANCO: tuple) -> None:
    """
    Dibuja el jugador en la pantalla.
    """
    pantalla.blit(player_image, player_data['rect'])

    if player_data['en_dash']:
        pygame.draw.rect(pantalla, BLANCO, player_data['rect'].inflate(10, 10), 2, border_radius=5)

def dibujar_disparos(pantalla: pygame.Surface, disparos_list: list) -> None:
    """
    Dibuja todos los disparos del jugador en la pantalla.
    """
    for disparo in disparos_list:
        pygame.draw.rect(pantalla, GREEN, disparo['rect'], border_radius=2) # Disparos verdes
