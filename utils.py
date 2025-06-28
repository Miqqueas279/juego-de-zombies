import pygame
import json
import os

# --- Funciones Auxiliares Generales ---

def get_font(size):
    """
    Obtiene una fuente por defecto de Pygame del tamaño especificado.
    Útil para asegurar que las fuentes estén disponibles.
    """
    return pygame.font.Font(None, size)

def detectar_colision_rect(rect1, rect2):
    """
    Detecta si dos objetos pygame.Rect están colisionando.
    """
    return rect1.colliderect(rect2)

def dibujar_texto(pantalla, texto, x, y, tamano_fuente, color, fuente=None):
    """
    Dibuja texto en la pantalla centrado en las coordenadas dadas.
    Si no se proporciona una fuente, usa una por defecto.
    """
    if fuente is None:
        fuente_obj = get_font(tamano_fuente) # Usar la función get_font
    else:
        fuente_obj = fuente

    superficie_texto = fuente_obj.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y))
    pantalla.blit(superficie_texto, rect_texto)

# --- Manejo de Puntajes (separado aquí para que juego.py y ranking.py lo importen) ---
# Asegúrate de que la carpeta 'datos' exista.
# Esto es para que funcione en entornos donde se ejecuta desde un directorio diferente
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORES_FILE = os.path.join(BASE_DIR, 'datos', 'puntajes.json')

def load_scores():
    """
    Carga los puntajes desde el archivo JSON.
    Si el archivo no existe o está vacío, devuelve una lista vacía.
    """
    if not os.path.exists(SCORES_FILE):
        return []
    # Abrir y cargar el archivo JSON si existe.
    with open(SCORES_FILE, 'r') as f:
        scores = json.load(f)
        # Asegurarse de que scores sea una lista
        # Si no es una lista, retornar una lista vacía para evitar errores
        if not isinstance(scores, list):
            return []
        return scores

def save_scores(scores):
    """
    Guarda los puntajes en el archivo JSON, ordenados por puntaje (descendente)
    y limitados al top 5.
    Crea la carpeta 'datos' si no existe.
    """
    # Ordenar los puntajes de mayor a menor sin list comprehension
    scores_a_ordenar = []
    for s in scores:
        scores_a_ordenar.append(s) # Copiar la lista

    # Algoritmo de burbuja para ordenar la lista sin sorted() ni list comprehension
    n = len(scores_a_ordenar)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if scores_a_ordenar[j]['puntaje'] < scores_a_ordenar[j+1]['puntaje']:
                scores_a_ordenar[j], scores_a_ordenar[j+1] = scores_a_ordenar[j+1], scores_a_ordenar[j]
    
    # Tomar los 5 mejores puntajes sin list comprehension
    top_5_scores = []
    count = 0
    for score in scores_a_ordenar:
        if count < 5:
            top_5_scores.append(score)
            count += 1
        else:
            break

    # Crear la carpeta 'datos' si no existe
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)

    with open(SCORES_FILE, 'w') as f:
        json.dump(top_5_scores, f, indent=4) # Guardar como JSON con formato legible
