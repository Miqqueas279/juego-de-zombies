import json
import os

# --- Manejo de puntajes (separado aquí para que juego.py y ranking.py lo importen) ---
# Asegúrate de que la carpeta 'datos' exista dentro de 'assets'.
# Esto es para que funcione en entornos donde se ejecuta desde un directorio diferente
# BASE_DIR será la carpeta raíz del proyecto (juego-de-zombies)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Apunta a la carpeta 'JUEGO-DE-ZOMBIES'
SCORES_FILE = os.path.join(BASE_DIR, 'assets', 'datos', 'puntajes.json') # Ruta corregida: assets/datos/puntajes.json

def load_scores():
    """
    Carga los puntajes desde el archivo JSON.
    Si el archivo no existe, devuelve una lista vacía.
    Si el contenido no es un JSON válido o no es una lista, devuelve una lista vacía.
    """
    if not os.path.exists(SCORES_FILE):
        return []
    
    with open(SCORES_FILE, 'r') as f:
        scores = json.load(f)
        # Asegurarse de que scores sea una lista
        if not isinstance(scores, list):
            return []
        return scores


def save_scores(scores):
    """
    Guarda los puntajes en el archivo JSON, ordenados por puntaje (descendente)
    y limitados al top 5.
    Crea la carpeta 'datos' si no existe.
    """
    # Ordenar los puntajes de mayor a menor (algoritmo de burbuja)
    scores_a_ordenar = []
    for s in scores:
        scores_a_ordenar.append(s) # Copiar la lista para operar sobre ella

    n = len(scores_a_ordenar)
    # Algoritmo de burbuja para ordenar
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if scores_a_ordenar[j]['puntaje'] < scores_a_ordenar[j+1]['puntaje']:
                scores_a_ordenar[j], scores_a_ordenar[j+1] = scores_a_ordenar[j+1], scores_a_ordenar[j]
    
    # Tomar los 5 mejores puntajes
    top_5_scores = []
    count = 0
    for score in scores_a_ordenar:
        if count < 5:
            top_5_scores.append(score)
            count += 1
        else:
            break

    # Crear la carpeta 'datos' si no existe
    # Asegúrate de que esta carpeta esté dentro de 'assets' como en tu estructura
    os.makedirs(os.path.dirname(SCORES_FILE), exist_ok=True)

    with open(SCORES_FILE, 'w') as f:
        json.dump(top_5_scores, f, indent=4) # Guardar como JSON con formato legible

def detectar_colision_rect(rect1, rect2):
    """
    Detecta si dos objetos pygame.Rect están colisionando.
    """
    return rect1.colliderect(rect2)
