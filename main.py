# ======================== main.py ========================

import pygame
import sys
from config import FPS, doodle_dict
from window import draw_window, show_game_over_message, generate_initial_platforms
from game import (
    apply_gravity, move_doodle, move_platforms,
    check_platform_collisions, scroll_camera,
    check_game_over, restart_game
)

# Initialisation de Pygame et de l'horloge
pygame.init()
clock = pygame.time.Clock()
running = True

# Génération initiale des plateformes avant de lancer la boucle
generate_initial_platforms()

# ======================== BOUCLE PRINCIPALE ========================
while running:
