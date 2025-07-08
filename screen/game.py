import math
import json
import os

import pygame
from entities.powerup import create_powerup, move_powerups, draw_powerups
from entities.enemy import draw_enemies, create_enemy, move_enemies
from entities.player import update_player_dash, draw_shoots, draw_player, shoot_player, init_player, move_shoots, move_player, use_player_dash
from screen.game_over import show_game_over
from utils.collision import detectar_colision_rect
from utils.image import get_image_from_spritesheet, load_image
from utils.soundtrack import play_music, load_sound
from utils.text import draw_text

# --- Funciones de Manejo de Entidades ---
def clean_off_screen_entities(enemy_list: list, shoot_list: list, powerups_list: list, screen_width: int) -> None:
    """
    Elimina enemigos, disparos y power-ups que han salido de la pantalla en un juego horizontal.
    Iteramos hacia atrás para poder eliminar elementos de la lista sin problemas de índice.
    """
    # Limpiar enemigos (que se mueven de derecha a izquierda)
    i = len(enemy_list) - 1
    while i >= 0:
        # Si el enemigo ha salido completamente por la izquierda
        if enemy_list[i]['rect'].right < 0:
            del enemy_list[i]
        i -= 1
    
    # Limpiar disparos (del jugador, que van hacia la derecha)
    i = len(shoot_list) - 1
    while i >= 0:
        # Si el disparo ha salido completamente por la derecha
        if shoot_list[i]['rect'].left > screen_width:
            del shoot_list[i]
        i -= 1
    
    # Limpiar power-ups (que se mueven de derecha a izquierda y ya no están activos)
    temp_powerups_list = []
    i = 0
    while i < len(powerups_list):
        if powerups_list[i]['activo'] and powerups_list[i]['rect'].right > 0:
            temp_powerups_list.append(powerups_list[i])
        i += 1
    # Asignar la lista filtrada de vuelta
    powerups_list[:] = temp_powerups_list # Esto modifica la lista original en su lugar


def handler_collisions(player_data, enemies_list, player_bullets_list, lost_health_sound: pygame.mixer.Sound | None, player_impact_sound: pygame.mixer.Sound | None, enemy_impact_sound: pygame.mixer.Sound | None) -> bool:
    """
    Detecta colisiones entre jugador, enemigos y balas.
    Devuelve True si el jugador pierde todas las vidas.
    """
    # Colisiones disparos vs enemigos
    i = len(player_bullets_list) - 1
    while i >= 0:
        bullet = player_bullets_list[i]
        j = len(enemies_list) - 1
        while j >= 0:
            enemy = enemies_list[j]
            if detectar_colision_rect(bullet['rect'], enemy['rect']):
                enemy['vida'] -= 1
                if enemy_impact_sound:
                    enemy_impact_sound.play()
                if enemy['vida'] <= 0:
                    player_data['puntos'] += enemy['puntos']
                    del enemies_list[j]
                del player_bullets_list[i]
                break
            j -= 1
        i -= 1

    # Colisiones enemigos vs jugador
    i = len(enemies_list) - 1
    while i >= 0:
        enemy = enemies_list[i]
        if detectar_colision_rect(player_data['rect'], enemy['rect']):
            player_data['vidas'] -= 1
            if player_impact_sound:
                player_impact_sound.play()
            if lost_health_sound:
                lost_health_sound.play()
            del enemies_list[i]
            print(f"[DEBUG] Vidas restantes: {player_data['vidas']}")
            if player_data['vidas'] <= 0:
                print("[DEBUG] Jugador sin vidas. Fin del juego.")
                return True
        i -= 1

    return False

def draw_health_bar(screen: pygame.Surface, actual_health: int, max_health: int, heart_image_surface: pygame.Surface, lost_heart_color: tuple) -> None:
    """
    Dibuja corazones llenos y vacíos hasta VIDAS_MAXIMAS.
    """
    x_offset = 10
    y_offset = 40
    spacing = heart_image_surface.get_width() + 5

    for i in range(max_health): # Iterar hasta VIDAS_MAXIMAS
        x = x_offset + i * spacing
        if i < actual_health:
            screen.blit(heart_image_surface, (x, y_offset))
        else:
            s = pygame.Surface(heart_image_surface.get_size(), pygame.SRCALPHA)
            s.fill(lost_heart_color)
            screen.blit(s, (x, y_offset))

def main_game_loop(screen: pygame.Surface, screen_size: dict, font_size: dict, colors: dict, player_config: dict, enemy_config: dict) -> tuple:
    """
    Gestiona la lógica principal de la partida.
    Retorna el puntaje final y el nombre del jugador si el juego termina.
    """
    player_spritesheet = load_image("player.png", player_config["frame_width"] * player_config["total_frames_per_row"], player_config["frame_height"] * 4, colors["blue"])
    background_image = load_image("floor.jpg", screen_size["width"], screen_size["height"], colors["black"])

    # Cargar la spritesheet del jugador
    powerup_image = {
        'vida': load_image("powerup_health.png", 30, 30, colors["green"]),
        'velocidad': load_image("powerup_speed.png", 30, 30, colors["blue"])
    }
    
    # Cargar las spritesheets de zombies para cada tipo
    zombie_spritesheets = {
        "normal": load_image("zombie1.png", enemy_config["frame_width"] * 3, enemy_config["frame_height"] * 4, colors["red"]),
        "boosted": load_image("zombie2.png", enemy_config["frame_width"] * 3, enemy_config["frame_height"] * 4, colors["green"]),
        "kamikaze": load_image("zombie3.png", enemy_config["frame_width"] * 3, enemy_config["frame_height"] * 4, colors["white"])
    }# Asumiendo 3x4 frames por spritesheet
        
    spritesheet_icons = load_image("icons.png", 256, 256, colors["red"], True)
    heart_surface_local = get_image_from_spritesheet(spritesheet_icons, (52, 0, 9, 9), (30, 30))

    bullet_image = load_image("bullet.png", 10, 7, (255,255,255))

    shoot_sound = load_sound("player_shoot.mp3", 0.1)
    recover_health_sound = load_sound("recover_health.mp3", 0.4)
    lost_health_sound = load_sound("lost_health.mp3", 0.4)
    increase_speed_sound = load_sound("increase_speed.mp3", 0.4)
    player_impact_sound = load_sound("player_impact.mp3", 0.3)
    enemy_impact_sound = load_sound("enemy_impact.mp3", 0.1)

    play_music("game_music.mp3", 0.05)

    clock = pygame.time.Clock()
    fps = 60 # Definir FPS aquí o cargar desde config.json

    # Inicializar datos del jugador
    player = init_player(screen_size["height"], player_config)
    
    # Listas para guardar enemigos y disparos
    enemies = []
    player_bullets = []
    powerups = [] # Lista para los power-ups

    frames_from_last_enemy_generation = 0 # Contador para la generación de enemigos
    frames_for_new_powerup = 0
    powerup_range_frames = 600  # cada 10 segundos (60 FPS * 10)

    running = True
    while running:
        # Obtener el tiempo actual en frames (o ticks)
        current_frames = pygame.time.get_ticks() // (1000 // fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None, None # Si el usuario cierra la ventana durante el juego
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Intentar disparar y añadir el nuevo disparo a la lista
                    new_shoot = shoot_player(player, current_frames, bullet_image, player_config)
                    if new_shoot:
                        if shoot_sound:
                            shoot_sound.play()
                        player_bullets.append(new_shoot)
                if event.key == pygame.K_z: # Tecla para el dash
                    use_player_dash(player, player_config)

        # --- Movimiento del Jugador ---
        keys = pygame.key.get_pressed()
        move_player(player, keys, screen_size["height"], player_config)
        update_player_dash(player) # Actualizar el temporizador del dash

        # --- Generación de Power-ups ---
        frames_for_new_powerup += 1
        if frames_for_new_powerup >= powerup_range_frames:
            powerups.append(create_powerup(screen_size["width"], screen_size["height"]))
            frames_for_new_powerup = 0
        
        # --- Generación de Enemigos ---
        frames_from_last_enemy_generation += 1
        if frames_from_last_enemy_generation >= enemy_config["generation_cooldown_ms"]:
            enemies.append(create_enemy(screen_size["width"], screen_size["height"], enemy_config))
            frames_from_last_enemy_generation = 0 # Reiniciar el contador

        # --- Movimiento de Entidades ---
        move_enemies(enemies)
        move_shoots(player_bullets)
        move_powerups(powerups)

        # --- Colisiones ---
        # Manejar colisiones entre jugador/enemigos/disparos
        game_over = handler_collisions(player, enemies, player_bullets, lost_health_sound, player_impact_sound, enemy_impact_sound)
        if game_over:
            running = False

        # Manejar colisiones entre jugador y power-ups
        for i in range(len(powerups) - 1, -1, -1):
            powerup = powerups[i]
            if player['rect'].colliderect(powerup['rect']):
                if powerup['tipo'] == 'vida' and player['vidas'] < player["max_health"]:
                    player['vidas'] += 1
                    if recover_health_sound:
                        recover_health_sound.play()
                elif powerup['tipo'] == 'velocidad':
                    player['velocidad'] += 1
                    if increase_speed_sound:
                        increase_speed_sound.play()
                del powerups[i] # Pasar VIDAS_MAXIMAS


        # --- Eliminar elementos fuera de pantalla ---
        clean_off_screen_entities(enemies, player_bullets, powerups, screen_size["width"])

        # --- Dibujar ---
        screen.blit(background_image, (0, 0))

        # Ahora pasamos la spritesheet del jugador a dibujar_jugador
        draw_player(screen, player, player_spritesheet, player_config, colors["white"]) 
        # Ahora pasamos el diccionario de spritesheets de zombies a dibujar_enemigos
        draw_enemies(screen, enemies, zombie_spritesheets, enemy_config) 
        draw_shoots(screen, player_bullets)
        draw_powerups(screen, powerups, powerup_image)

        # Dibujar UI (vidas y puntaje)
        # Ajustar posición del puntaje para el layout horizontal
        draw_text(screen, f"Puntaje: {player['puntos']}\n", 15, 20, 24, colors["white"], "left") # Agregué un salto de línea para separar del dash CD
        draw_health_bar(screen, player['vidas'], player_config["max_health"], heart_surface_local, player_config["lost_health_color"])
        
        # Mostrar el estado del dash cooldown
        if player['dash_cooldown_timer'] > 0:
            tiempo_restante_dash = math.ceil(player['dash_cooldown_timer'] / fps)
            draw_text(screen, f"Dash CD: {tiempo_restante_dash}s", screen_size["width"] - 110, 20, 24, colors["red"], "left")
        elif not player['en_dash']:
            draw_text(screen, "Dash Listo", screen_size["width"] - 110, 20, 24, colors["green"], "left")
        
        pygame.display.flip() # Actualizar toda la pantalla
        
        clock.tick(fps) # Controlar los FPS del juego

    puntos, nombre = show_game_over(screen, screen_size, font_size, colors, player)

    return puntos, nombre
