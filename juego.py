import pygame
import random
import math
from utils import dibujar_texto, detectar_colision_rect, get_font # Importar funciones auxiliares

# --- Constantes del Juego ---
COLOR_JUGADOR = (0, 0, 255)  # Azul
COLOR_NORMAL_ENEMY = (255, 0, 0) # Rojo
COLOR_BOOSTED_ENEMY = (255, 100, 0) # Naranja (más rápido)
COLOR_KAMIKAZE_ENEMY = (255, 255, 0) # Amarillo (kamikaze)
COLOR_DISPARO_JUGADOR = (0, 255, 0) # Verde

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


# --- Funciones de Manejo de Entidades ---

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

def dibujar_jugador(pantalla, player_data, AZUL, BLANCO):
    """
    Dibuja el jugador en la pantalla.
    """
    if player_data['en_dash']:
        # Dibujar un color diferente o efecto para el dash
        pygame.draw.rect(pantalla, AZUL, player_data['rect'], border_radius=5)
        # Borde blanco para efecto de dash
        pygame.draw.rect(pantalla, BLANCO, player_data['rect'].inflate(10, 10), 2, border_radius=5)
    else:
        pygame.draw.rect(pantalla, COLOR_JUGADOR, player_data['rect'], border_radius=5)


def generar_enemigo(ANCHO_PANTALLA):
    """
    Crea un nuevo diccionario de enemigo con propiedades aleatorias.
    """
    enemy_ancho = 40
    enemy_alto = 40
    # Posición X aleatoria en la parte superior
    x_pos = random.randint(enemy_ancho // 2, ANCHO_PANTALLA - enemy_ancho // 2)
    y_pos = -enemy_alto # Empieza justo fuera de la pantalla por arriba

    # Propiedades base
    velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE
    vida_enemigo = 1
    color_enemigo = COLOR_NORMAL_ENEMY
    puntaje_enemigo = PUNTAJE_NORMAL
    tipo_enemigo = "normal"

    # Determinar tipo de enemigo especial
    r = random.random()
    if r < PROBABILIDAD_KAMIKAZE:
        tipo_enemigo = "kamikaze"
        velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE * FACTOR_VELOCIDAD_KAMIKAZE
        vida_enemigo = VIDA_KAMIKAZE
        color_enemigo = COLOR_KAMIKAZE_ENEMY
        puntaje_enemigo = PUNTAJE_KAMIKAZE
    elif r < PROBABILIDAD_KAMIKAZE + PROBABILIDAD_BOOSTED: # Suma las probabilidades para que no se solapen
        tipo_enemigo = "boosted"
        velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE * FACTOR_VELOCIDAD_BOOSTED
        color_enemigo = COLOR_BOOSTED_ENEMY
        puntaje_enemigo = PUNTAJE_BOOSTED
    
    return {
        'rect': pygame.Rect(x_pos - enemy_ancho // 2, y_pos - enemy_alto // 2, enemy_ancho, enemy_alto),
        'velocidad': velocidad_enemigo,
        'vida': vida_enemigo,
        'tipo': tipo_enemigo,
        'color': color_enemigo,
        'puntos': puntaje_enemigo # Puntos que otorga al ser destruido
    }

def mover_enemigos(enemigos_list):
    """
    Actualiza la posición de todos los enemigos en la lista.
    """
    for enemigo in enemigos_list:
        enemigo['rect'].y += enemigo['velocidad']

def dibujar_enemigos(pantalla, enemigos_list):
    """
    Dibuja todos los enemigos en la pantalla.
    """
    for enemigo in enemigos_list:
        pygame.draw.rect(pantalla, enemigo['color'], enemigo['rect'], border_radius=3)

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
            del enemigos_list[i_enemy] # El enemigo se destruye al impactar al jugador
            if player_data['vidas'] <= 0:
                game_over = True # Juego terminado
                break # No es necesario seguir revisando enemigos
        i_enemy -= 1
    
    return game_over


# --- Bucle Principal del Juego (main_game_loop) ---
def main_game_loop(pantalla, ANCHO_PANTALLA, ALTO_PANTALLA, fuente_pequena, NEGRO, BLANCO, ROJO, VERDE, AZUL):
    """
    Gestiona la lógica principal de la partida.
    Retorna el puntaje final y el nombre del jugador si el juego termina.
    """
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
        pantalla.fill(NEGRO) # Rellenar el fondo de negro (pueden reemplazarlo con una imagen)

        dibujar_jugador(pantalla, player, AZUL, BLANCO) # Dibujar el jugador
        dibujar_enemigos(pantalla, enemigos) # Dibujar todos los enemigos
        dibujar_disparos(pantalla, player_bullets) # Dibujar todos los disparos del jugador

        # Dibujar UI (vidas y puntaje)
        dibujar_texto(pantalla, f"Puntaje: {player['puntos']}", 10, 10, 24, BLANCO, fuente=fuente_pequena)
        dibujar_texto(pantalla, f"Vidas: {player['vidas']}", 10, 40, 24, BLANCO, fuente=fuente_pequena)
        
        # Mostrar el estado del dash cooldown
        if player['dash_cooldown_timer'] > 0:
            tiempo_restante_dash = math.ceil(player['dash_cooldown_timer'] / fps)
            dibujar_texto(pantalla, f"Dash CD: {tiempo_restante_dash}s", ANCHO_PANTALLA - 150, 10, 24, ROJO, fuente=fuente_pequena)
        elif not player['en_dash']:
            dibujar_texto(pantalla, "Dash Listo", ANCHO_PANTALLA - 150, 10, 24, VERDE, fuente=fuente_pequena)


        pygame.display.flip() # Actualizar toda la pantalla

        reloj.tick(fps) # Controlar los FPS del juego

    # --- Game Over Screen ---
    # Pedir nombre al jugador después de que el bucle principal del juego termina
    nombre_ingresado = ""
    input_activo = True
    # Usar una fuente diferente para esta pantalla si es necesario
    game_over_font_title = get_font(74)
    game_over_font_score = get_font(36)
    game_over_font_input = get_font(36)

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
        dibujar_texto(pantalla, "GAME OVER", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 50, 74, ROJO, fuente=game_over_font_title)
        dibujar_texto(pantalla, f"Puntaje Final: {player['puntos']}", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 20, 36, BLANCO, fuente=game_over_font_score)
        dibujar_texto(pantalla, "Ingresa tu nombre:", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 80, 36, BLANCO, fuente=game_over_font_input)
        dibujar_texto(pantalla, nombre_ingresado + "|", ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 120, 36, BLANCO, fuente=game_over_font_input) # El "|" simula el cursor
        pygame.display.flip()

    return player['puntos'], nombre_ingresado # Devolver el puntaje y el nombre para guardar
