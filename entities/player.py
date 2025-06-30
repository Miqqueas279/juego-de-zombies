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
    Inicializa los datos del jugador como un diccionario.
    """
    player_ancho = 50
    player_alto = 50
    return {
        'rect': pygame.Rect(ANCHO_PANTALLA // 2 - player_ancho // 2, ALTO_PANTALLA - 70 - player_alto // 2, player_ancho, player_alto),
        'velocidad': VELOCIDAD_JUGADOR_BASE,
        'vidas': VIDAS_INICIALES,
        'puntos': 0,
        'ultima_vez_disparo': 0, # Tiempo en frames desde el último disparo
        'cooldown_disparo': 20, # Frames a esperar entre disparos
        'en_dash': False,
        'dash_timer': 0,
        'dash_cooldown_timer': 0
    }

def mover_jugador(player_data, keys, ANCHO_PANTALLA):
    """
    Actualiza la posición del jugador según las teclas presionadas.
    """
    current_speed = player_data['velocidad']
    if player_data['en_dash']:
        current_speed *= DASH_VELOCIDAD_MULTIPLIER

    if keys[pygame.K_LEFT]:
        player_data['rect'].x -= current_speed
    if keys[pygame.K_RIGHT]:
        player_data['rect'].x += current_speed

    # Limitar el movimiento dentro de la pantalla
    if player_data['rect'].left < 0:
        player_data['rect'].left = 0
    if player_data['rect'].right > ANCHO_PANTALLA:
        player_data['rect'].right = ANCHO_PANTALLA

def disparar_jugador(player_data, current_frames):
    """
    Crea un nuevo diccionario de disparo si el cooldown lo permite.
    """
    if current_frames - player_data['ultima_vez_disparo'] > player_data['cooldown_disparo']:
        player_data['ultima_vez_disparo'] = current_frames
        bullet_ancho = 5
        bullet_alto = 15
        return {
            'rect': pygame.Rect(player_data['rect'].centerx - bullet_ancho // 2, player_data['rect'].top - bullet_alto, bullet_ancho, bullet_alto),
            'velocidad': VELOCIDAD_DISPARO_JUGADOR,
            'color': GREEN,
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
        return True # Dash activado
    return False # Dash no activado (en cooldown)

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

def dibujar_jugador(pantalla, player_data, player_image, AZUL, BLANCO):
    """
    Dibuja el jugador en la pantalla.
    """

    pantalla.blit(player_image, player_data['rect'])

    if player_data['en_dash']:
        pygame.draw.rect(pantalla, BLANCO, player_data['rect'].inflate(10, 10), 2, border_radius=5)

    #if player_data['en_dash']:
    #   # Dibujar un color diferente o efecto para el dash
    #    pygame.draw.rect(pantalla, AZUL, player_data['rect'], border_radius=5)
    #    # Borde blanco para efecto de dash
    #    pygame.draw.rect(pantalla, BLANCO, player_data['rect'].inflate(10, 10), 2, border_radius=5)
    #else:
    #    pygame.draw.rect(pantalla, COLOR_JUGADOR, player_data['rect'], border_radius=5)

def mover_disparos(disparos_list):
    """
    Actualiza la posición de todos los disparos en la lista.
    """
    for disparo in disparos_list:
        # En este juego, los disparos del jugador van hacia arriba
        disparo['rect'].y -= disparo['velocidad']

def dibujar_disparos(pantalla, disparos_list):
    """
    Dibuja todos los disparos en la pantalla.
    """

    for disparo in disparos_list:
        pygame.draw.rect(pantalla, disparo['color'], disparo['rect'])