import random

import pygame

BASE_ENEMY_SPEED = 2
# Probabilidades de tipos de enemigos
PROBABILITY_BOOSTED = 0.2 # 20% de probabilidad de enemigo con boost
PROBABILITY_KAMIKAZE = 0.1 # 10% de probabilidad de kamikaze
# Multiplicadores de velocidad para enemigos especiales
FACTOR_VELOCIDAD_BOOSTED =  0.5 # Los enemigos con boost son 50% más rápidos
FACTOR_VELOCIDAD_KAMIKAZE = 3.0 # Los kamikazes son 200% más rápidos
HEALTH_KAMIKAZE = 1 # Los kamikazes tienen poca vida
HEALTH_BOOSTED = 3
# Puntos que otorgan los enemigos
SCORE_NORMAL = 10
SCORE_BOOSTED = 15
SCORE_KAMIKAZE = 25

# --- Constantes de Animación para Zombies ---
# Asegúrate de que estos valores coincidan con tu spritesheet de zombies
ZOMBIE_FRAME_WIDTH = 40 # Ancho de un solo frame en la spritesheet
ZOMBIE_FRAME_HEIGHT = 40 # Alto de un solo frame en la spritesheet
ZOMBIE_TOTAL_FRAMES = 3 # Número total de frames en la animación de caminata (asumiendo 3 frames por fila para la caminata)
ZOMBIE_ANIMATION_SPEED_FPS = 5 # Cuántos frames del juego antes de cambiar al siguiente frame de animación

def create_enemy(scree_width: int, scree_height: int) -> dict:
    """
    Crea un nuevo diccionario de enemigo con propiedades aleatorias para un juego horizontal.
    Los enemigos aparecen en el lado derecho de la pantalla y se mueven hacia la izquierda.
    Ahora incluye propiedades para la animación.
    """
    enemy_width = ZOMBIE_FRAME_WIDTH # Usamos el tamaño del frame para el rectángulo de colisión
    enemy_height = ZOMBIE_FRAME_HEIGHT

    # Posición Y aleatoria en la pantalla
    y_pos = random.randint(enemy_height // 2, scree_height - enemy_height // 2)
    # Posición X: empieza justo fuera de la pantalla por la derecha
    x_pos = scree_width + enemy_width # Empieza fuera de la pantalla por la derecha

    # Propiedades base
    enemy_speed = BASE_ENEMY_SPEED
    enemy_health = 2
    enemy_score = SCORE_NORMAL
    enemy_type = "normal"

    # Determinar tipo de enemigo especial
    r = random.random()
    if r < PROBABILITY_KAMIKAZE:
        enemy_type = "kamikaze"
        enemy_speed = BASE_ENEMY_SPEED * FACTOR_VELOCIDAD_KAMIKAZE
        enemy_health = HEALTH_KAMIKAZE
        enemy_score = SCORE_KAMIKAZE
    elif r < PROBABILITY_KAMIKAZE + PROBABILITY_BOOSTED: # Suma las probabilidades para que no se solapen
        enemy_type = "boosted"
        enemy_speed = BASE_ENEMY_SPEED * FACTOR_VELOCIDAD_BOOSTED
        enemy_score = SCORE_BOOSTED
        enemy_health = HEALTH_BOOSTED
    
    # La velocidad es negativa para que se muevan hacia la izquierda
    return {
        'rect': pygame.Rect(x_pos - enemy_width // 2, y_pos - enemy_height // 2, enemy_width, enemy_height),
        'velocidad': -enemy_speed, # Ahora la velocidad es negativa para ir a la izquierda
        'vida': enemy_health,
        'tipo': enemy_type,
        'puntos': enemy_score, # Puntos que otorga al ser destruido
        'current_frame': 0, # Frame actual de la animación
        'animation_timer': 0 # Temporizador para controlar la velocidad de la animación
    }

def move_enemies(enemies_list: list) -> None:
    """
    Mueve todos los enemigos horizontalmente hacia la izquierda.
    """
    for enemy in enemies_list:
        # Mover horizontalmente
        enemy['rect'].x += enemy['velocidad']


def draw_enemies(screen: pygame.Surface, enemies_list: list, zombie_spritesheets: dict) -> None:
    """
    Dibuja todos los enemigos en la pantalla, usando su animación y la spritesheet correcta según su tipo.
    """
    for enemy in enemies_list:
        # Obtener la spritesheet correcta para este tipo de enemigo
        current_zombie_spritesheet = zombie_spritesheets.get(enemy['tipo'])
        
        if current_zombie_spritesheet: # Asegurarse de que la spritesheet exista
            # Actualizar el temporizador de animación
            enemy['animation_timer'] += 1
            if enemy['animation_timer'] >= ZOMBIE_ANIMATION_SPEED_FPS:
                enemy['animation_timer'] = 0
                enemy['current_frame'] = (enemy['current_frame'] + 1) % ZOMBIE_TOTAL_FRAMES

            # Calcular el área del frame actual en la spritesheet
            frame_x = enemy['current_frame'] * ZOMBIE_FRAME_WIDTH
            frame_y = 41 # lógica de que fila usamos para la animación
            frame_rect = pygame.Rect(frame_x, frame_y, ZOMBIE_FRAME_WIDTH, ZOMBIE_FRAME_HEIGHT)
            
            # Extraer el frame actual de la spritesheet
            current_frame_image = current_zombie_spritesheet.subsurface(frame_rect)

            # Dibujar el frame actual en la posición del enemigo
            screen.blit(current_frame_image, enemy['rect'])