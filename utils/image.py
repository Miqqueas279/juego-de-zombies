import os

import pygame

def load_image(image_name: str, width: int, height: int, color: tuple, is_spritesheet: bool = False) -> pygame.Surface:
    """
    Carga una imagen y la hace escalar a un tamaño específico, sino se encuentra,
    crea un cuadrado de color como reemplazo y avisa en la consola. 
    """

    image_path = os.path.join("assets", "image", image_name)

    if not os.path.exists(image_path):
        placeholder = pygame.Surface((width, height))
        placeholder.fill(color) 

        print(f"[ERROR] Archivo de imagen no encontrado: {image_path}") 
        return placeholder
    
    image = pygame.image.load(image_path).convert_alpha()

    if not is_spritesheet:
        image = pygame.transform.scale(image, (width, height))
    
    return image

def get_image_from_spritesheet(spritesheet: pygame.Surface, icon_delimiter: tuple, icon_size: tuple):
    """
    Extrae un frame de un spritesheet. 
    Luego, escala ese frame al tamaño que necesites. 
    """

    icon = spritesheet.subsurface(pygame.Rect(icon_delimiter))     
    icon = pygame.transform.scale(icon, icon_size)

    return icon