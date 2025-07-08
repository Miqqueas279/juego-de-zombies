import random

import pygame

def create_enemy(screen_width: int, screen_height: int, enemy_config: dict) -> dict:
    """
    Crea un nuevo diccionario de enemigo con propiedades aleatorias para un juego horizontal.
    Los enemigos aparecen en el lado derecho de la pantalla y se mueven hacia la izquierda.
    Ahora incluye propiedades para la animación.
    """
    # Posición Y aleatoria en la pantalla
    y_pos = random.randint(enemy_config["frame_height"] // 2, screen_height - enemy_config["frame_height"] // 2)
    # Posición X: empieza justo fuera de la pantalla por la derecha
    x_pos = screen_width + enemy_config["frame_width"] # Empieza fuera de la pantalla por la derecha

    # Propiedades base
    enemy_speed = enemy_config["speed"]
    enemy_health = enemy_config["health"]
    enemy_score = enemy_config["score_normal"]
    enemy_type = "normal"

    # Determinar tipo de enemigo especial
    r = random.random()
    if r < enemy_config["probability_kamikaze"]:
        enemy_type = "kamikaze"
        enemy_speed = enemy_config["speed"] * enemy_config["speed_kamikaze"]
        enemy_health = enemy_config["health_kamikaze"]
        enemy_score = enemy_config["score_kamikaze"]
    elif r < enemy_config["probability_kamikaze"] + enemy_config["probability_boosted"]: # Suma las probabilidades para que no se solapen
        enemy_type = "boosted"
        enemy_speed = enemy_config["speed"] * enemy_config["speed_boosted"]
        enemy_score = enemy_config["score_boosted"]
        enemy_health = enemy_config["health_boosted"]
    
    # La velocidad es negativa para que se muevan hacia la izquierda
    return {
        'rect': pygame.Rect(x_pos - enemy_config["frame_width"] // 2, y_pos - enemy_config["frame_height"] // 2, enemy_config["frame_width"], enemy_config["frame_height"]),
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


def draw_enemies(screen: pygame.Surface, enemies_list: list, zombie_spritesheets: dict, enemy_config: dict) -> None:
    """
    Dibuja todos los enemigos en la pantalla, usando su animación y la spritesheet correcta según su tipo.
    """
    for enemy in enemies_list:
        # Obtener la spritesheet correcta para este tipo de enemigo
        current_zombie_spritesheet = zombie_spritesheets.get(enemy['tipo'])
        
        if current_zombie_spritesheet: # Asegurarse de que la spritesheet exista
            # Actualizar el temporizador de animación
            enemy['animation_timer'] += 1
            if enemy['animation_timer'] >= enemy_config["animation_speed_fps"]:
                enemy['animation_timer'] = 0
                enemy['current_frame'] = (enemy['current_frame'] + 1) % enemy_config["total_frames"]

            # Calcular el área del frame actual en la spritesheet
            frame_x = enemy['current_frame'] * enemy_config["frame_width"]
            frame_y = 41 # lógica de que fila usamos para la animación
            frame_rect = pygame.Rect(frame_x, frame_y, enemy_config["frame_width"], enemy_config["frame_height"])
            
            # Extraer el frame actual de la spritesheet
            current_frame_image = current_zombie_spritesheet.subsurface(frame_rect)

            # Dibujar el frame actual en la posición del enemigo
            screen.blit(current_frame_image, enemy['rect'])