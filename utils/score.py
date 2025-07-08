import json
import os

def load_scores() -> list:
    """
    Carga los puntajes desde el archivo JSON.
    Si el archivo no existe o está vacío, devuelve una lista vacía.
    """
    score_file_path = os.path.join("score.json")

    if not os.path.exists(score_file_path):
        return []
    
    # Abrir y cargar el archivo JSON si existe.
    with open(score_file_path, 'r') as file:
        scores = json.load(file)
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
    score_file_path = os.path.join("score.json")

    # Ordenar los puntajes de mayor a menor 
    scores_a_ordenar = []
    for s in scores:
        scores_a_ordenar.append(s) # Copiar la lista

    # Algoritmo de burbuja para ordenar la lista
    n = len(scores_a_ordenar)
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

    with open(score_file_path, 'w') as file:
        json.dump(top_5_scores, file, indent=4) # Guardar como JSON con formato legible