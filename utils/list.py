def copy_list(old_list: list) -> list:
    """
    Crea y devuelve una copia superficial de una lista.
    """
    new_list = []

    for item in old_list:
        new_list.append(item)

    return new_list


def sort_list(unordered_list: list[dict], key: str, limit: int) -> list[dict]:
    """
    Ordena una lista de diccionarios de forma descendente según un valor de clave,
    y devuelve los primeros 'limit' elementos.
    """
    new_list = copy_list(unordered_list)
    length = len(new_list)
    limit_list = []

    # Ordenamiento burbuja descendente
    for i in range(length):
        for j in range(0, length - i - 1):
            if new_list[j][key] < new_list[j + 1][key]:
                # Intercambio de elementos
                new_list[j], new_list[j + 1] = new_list[j + 1], new_list[j]

    # Tomar hasta 'limit' elementos de la lista ordenada
    for i in range(min(length, limit)):
        limit_list.append(new_list[i])

    return limit_list
