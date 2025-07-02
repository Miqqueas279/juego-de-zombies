import pygame
import random

VELOCIDAD_ENEMIGO_BASE = 2
# Probabilidades de tipos de enemigos
PROBABILIDAD_BOOSTED = 0.2 # 20% de probabilidad de enemigo con boost
PROBABILIDAD_KAMIKAZE = 0.1 # 10% de probabilidad de kamikaze
# Multiplicadores de velocidad para enemigos especiales
FACTOR_VELOCIDAD_BOOSTED =  0.5 # Los enemigos con boost son 50% más rápidos
FACTOR_VELOCIDAD_KAMIKAZE = 3.0 # Los kamikazes son 200% más rápidos
VIDA_KAMIKAZE = 1 # Los kamikazes tienen poca vida
VIDA_BOOSTED = 3
# Puntos que otorgan los enemigos
PUNTAJE_NORMAL = 10
PUNTAJE_BOOSTED = 15
PUNTAJE_KAMIKAZE = 25

# --- Constantes de Animación para Zombies ---
# Asegúrate de que estos valores coincidan con tu spritesheet de zombies
ZOMBIE_FRAME_WIDTH = 40 # Ancho de un solo frame en la spritesheet
ZOMBIE_FRAME_HEIGHT = 40 # Alto de un solo frame en la spritesheet
ZOMBIE_TOTAL_FRAMES = 3 # Número total de frames en la animación de caminata (asumiendo 3 frames por fila para la caminata)
ZOMBIE_ANIMATION_SPEED_FPS = 5 # Cuántos frames del juego antes de cambiar al siguiente frame de animación

def generar_enemigo(ANCHO_PANTALLA: int, ALTO_PANTALLA: int) -> dict:
    """
    Crea un nuevo diccionario de enemigo con propiedades aleatorias para un juego horizontal.
    Los enemigos aparecen en el lado derecho de la pantalla y se mueven hacia la izquierda.
    Ahora incluye propiedades para la animación.
    """
    enemy_ancho = ZOMBIE_FRAME_WIDTH # Usamos el tamaño del frame para el rectángulo de colisión
    enemy_alto = ZOMBIE_FRAME_HEIGHT

    # Posición Y aleatoria en la pantalla
    y_pos = random.randint(enemy_alto // 2, ALTO_PANTALLA - enemy_alto // 2)
    # Posición X: empieza justo fuera de la pantalla por la derecha
    x_pos = ANCHO_PANTALLA + enemy_ancho # Empieza fuera de la pantalla por la derecha

    # Propiedades base
    velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE
    vida_enemigo = 2
    puntaje_enemigo = PUNTAJE_NORMAL
    tipo_enemigo = "normal"

    # Determinar tipo de enemigo especial
    r = random.random()
    if r < PROBABILIDAD_KAMIKAZE:
        tipo_enemigo = "kamikaze"
        velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE * FACTOR_VELOCIDAD_KAMIKAZE
        vida_enemigo = VIDA_KAMIKAZE
        puntaje_enemigo = PUNTAJE_KAMIKAZE
    elif r < PROBABILIDAD_KAMIKAZE + PROBABILIDAD_BOOSTED: # Suma las probabilidades para que no se solapen
        tipo_enemigo = "boosted"
        velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE * FACTOR_VELOCIDAD_BOOSTED
        puntaje_enemigo = PUNTAJE_BOOSTED
        vida_enemigo = VIDA_BOOSTED
    
    # La velocidad es negativa para que se muevan hacia la izquierda
    return {
        'rect': pygame.Rect(x_pos - enemy_ancho // 2, y_pos - enemy_alto // 2, enemy_ancho, enemy_alto),
        'velocidad': -velocidad_enemigo, # Ahora la velocidad es negativa para ir a la izquierda
        'vida': vida_enemigo,
        'tipo': tipo_enemigo,
        'puntos': puntaje_enemigo, # Puntos que otorga al ser destruido
        'current_frame': 0, # Frame actual de la animación
        'animation_timer': 0 # Temporizador para controlar la velocidad de la animación
    }

def mover_enemigos(enemigos_list: list, player_data: dict | None = None) -> None:
    """
    Mueve todos los enemigos horizontalmente hacia la izquierda.
    """
    for enemy in enemigos_list:
        # Mover horizontalmente
        enemy['rect'].x += enemy['velocidad']


def dibujar_enemigos(pantalla: pygame.Surface, enemigos_list: list, zombie_spritesheets: dict) -> None:
    """
    Dibuja todos los enemigos en la pantalla, usando su animación y la spritesheet correcta según su tipo.
    """
    for enemy in enemigos_list:
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
            frame_y = 41 # logica de que fila usamos para la animacion
            frame_rect = pygame.Rect(frame_x, frame_y, ZOMBIE_FRAME_WIDTH, ZOMBIE_FRAME_HEIGHT)
            
            # Extraer el frame actual de la spritesheet
            current_frame_image = current_zombie_spritesheet.subsurface(frame_rect)

            # Dibujar el frame actual en la posición del enemigo
            pantalla.blit(current_frame_image, enemy['rect'])
