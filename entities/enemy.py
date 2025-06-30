import pygame
import random

VELOCIDAD_ENEMIGO_BASE = 2
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

def generar_enemigo(ANCHO_PANTALLA: int, ALTO_PANTALLA: int) -> dict:
    """
    Crea un nuevo diccionario de enemigo con propiedades aleatorias para un juego horizontal.
    Los enemigos aparecen en el lado derecho de la pantalla y se mueven hacia la izquierda.
    """
    enemy_ancho = 40
    enemy_alto = 40
    # Posición Y aleatoria en la pantalla
    y_pos = random.randint(enemy_alto // 2, ALTO_PANTALLA - enemy_alto // 2)
    # Posición X: empieza justo fuera de la pantalla por la derecha
    x_pos = ANCHO_PANTALLA + enemy_ancho # Empieza fuera de la pantalla por la derecha

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
    elif r < PROBABILIDAD_KAMIKAZE + PROBABILIDAD_BOOSTED: # Suma las probabilidades para que no se solapen
        tipo_enemigo = "boosted"
        velocidad_enemigo = VELOCIDAD_ENEMIGO_BASE * FACTOR_VELOCIDAD_BOOSTED
        puntaje_enemigo = PUNTAJE_BOOSTED
    
    # La velocidad es negativa para que se muevan hacia la izquierda
    return {
        'rect': pygame.Rect(x_pos - enemy_ancho // 2, y_pos - enemy_alto // 2, enemy_ancho, enemy_alto),
        'velocidad': -velocidad_enemigo, # Ahora la velocidad es negativa para ir a la izquierda
        'vida': vida_enemigo,
        'tipo': tipo_enemigo,
        'puntos': puntaje_enemigo # Puntos que otorga al ser destruido
    }

def mover_enemigos(enemigos_list: list, player_data: dict | None = None) -> None:
    """
    Mueve todos los enemigos horizontalmente hacia la izquierda.
    Los enemigos kamikaze ahora también solo se moverán horizontalmente.
    """
    for enemy in enemigos_list:
        # Mover horizontalmente
        enemy['rect'].x += enemy['velocidad']

        # La lógica de persecución en Y para kamikazes ha sido eliminada.
        # Ahora, los kamikazes también se mueven solo horizontalmente.


def dibujar_enemigos(pantalla: pygame.Surface, enemigos_list: list, enemy_image: pygame.Surface) -> None:
    """
    Dibuja todos los enemigos en la pantalla.
    """
    for enemy in enemigos_list:
        pantalla.blit(enemy_image, enemy['rect'])
        # Opcional: Dibujar la vida del enemigo si es más de 1
        # if enemy['vida'] > 1:
        #     pygame.draw.rect(pantalla, (255, 0, 0), (enemy['rect'].x, enemy['rect'].y - 10, enemy['rect'].width, 5))
        #     pygame.draw.rect(pantalla, (0, 255, 0), (enemy['rect'].x, enemy['rect'].y - 10, enemy['rect'].width * (enemy['vida'] / VIDA_MAXIMA_ENEMIGO), 5))
