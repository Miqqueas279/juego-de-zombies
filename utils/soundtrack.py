import os
import pygame

def play_music(music_name: str, volume: float) -> None:
    """
    Ingresa el nombre de la musica conjunto al volumen deseado y comprueba si existe
    Si es asi, lo reproduce infinitamente y sino printea un mensaje para que no rompa el juego.
    """
    music_path = os.path.join("assets", "sounds", music_name)

    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    else:
        print(f"[ERROR] Archivo de música no encontrado: {music_path}") 
    
def stop_music() -> None:
    """
    Detiene la musica
    """
    pygame.mixer.music.stop()

def load_sound(sound_name: str, volume: float) -> pygame.mixer.Sound | None:
    """
    Ingresa el nombre del sonido conjunto al volumen deseado y comprueba si existe
    Si es asi, lo reproduce y sino printea un mensaje para que no rompa el juego.
    """
    sound_path = os.path.join("assets", "sounds", sound_name)

    if os.path.exists(sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(volume)
    else:
        print(f"[ERROR] Archivo de sonido no encontrado: {sound_path}") 

    return sound