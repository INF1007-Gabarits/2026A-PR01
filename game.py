# ======================== game.py ========================

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_VELOCITY, SPRING_JUMP_VELOCITY,
    DOODLE_SPEED, DOODLE_WIDTH, DOODLE_HEIGHT, PLATFORM_WIDTH,
    MIN_PLATFORM_GAP, MAX_PLATFORM_GAP, CAMERA_SCROLL_THRESHOLD,
    PLATFORMS, doodle_dict, DOODLE_START_X, DOODLE_START_Y, LIVES
)
from platforms import create_platform, choose_platform_type
from doodle import doodle_left_img, doodle_right_img
from window import generate_initial_platforms


# ======================== PARTIE 3.1 — CORRIGÉ ========================
def apply_gravity():
    """
    Applique la gravité au Doodle en augmentant progressivement sa vitesse verticale (vel_y).
    Met à jour la position verticale (y) du Doodle.
    """
    doodle_dict["vel_y"] += GRAVITY
    doodle_dict["y"] += doodle_dict["vel_y"]
# =====================================================================


# ======================== PARTIE 1.2 — CORRIGÉ ========================
def move_doodle():
    """
    Gère le déplacement horizontal du Doodle selon les touches pressées (Flèches ou A/D).
    Implémente le passage fluide d'un côté de l'écran à l'autre (Screen Wrap).
    """
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        doodle_dict["x"] -= DOODLE_SPEED
        doodle_dict["direction"] = "left"
        doodle_dict["image"] = doodle_left_img
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        doodle_dict["x"] += DOODLE_SPEED
        doodle_dict["direction"] = "right"
        doodle_dict["image"] = doodle_right_img

    # Une partie du Doodle peut sortir de l'écran avant le passage de l'autre côté.
    if doodle_dict["x"] < -DOODLE_WIDTH // 2:
        doodle_dict["x"] = SCREEN_WIDTH - DOODLE_WIDTH // 2
    elif doodle_dict["x"] > SCREEN_WIDTH - DOODLE_WIDTH // 2:
        doodle_dict["x"] = -DOODLE_WIDTH // 2
# =====================================================================


# ======================== PARTIE 2.3 — CORRIGÉ ========================
def move_platforms():
    """
    Déplace horizontalement les plateformes mobiles ("blue").
    Fait rebondir les plateformes lorsqu'elles atteignent les bords de la fenêtre.
    """
    for p in PLATFORMS:
        if p["type"] != "blue" or not p["active"]:
            continue

        p["x"] += p["vx"]

        if p["x"] <= 0:
            p["x"] = 0.0
            p["vx"] = abs(p["vx"])
        elif p["x"] + p["width"] >= SCREEN_WIDTH:
            p["x"] = float(SCREEN_WIDTH - p["width"])
            p["vx"] = -abs(p["vx"])
# =====================================================================


# ======================== PARTIE 3.2 — CORRIGÉ ========================
def check_platform_collisions():
    """
    Détecte si le Doodle atterrit sur une plateforme.
    Le rebond ne se produit QUE lorsque le Doodle descend (vel_y > 0)
    et qu'il arrive sur le dessus d'une plateforme.
    """
    if doodle_dict["vel_y"] <= 0:
        return

    doodle_rect = (
        doodle_dict["x"], doodle_dict["y"],
        DOODLE_WIDTH, DOODLE_HEIGHT
    )
    doodle_feet = doodle_dict["y"] + DOODLE_HEIGHT
    previous_doodle_feet = doodle_feet - doodle_dict["vel_y"]

    for p in PLATFORMS:
        if not p["active"]:
            continue

        platform_rect = (p["x"], p["y"], p["width"], p["height"])

        if not rects_collide(doodle_rect, platform_rect):
            continue

        # Le Doodle doit avoir franchi le dessus de la plateforme entre
        # l'image précédente et l'image actuelle. La tolérance de 14 px
        # évite de manquer un atterrissage à cause du déplacement entre frames.
        if previous_doodle_feet <= p["y"] + 14:
            if p["type"] == "spring":
                doodle_dict["vel_y"] = SPRING_JUMP_VELOCITY
            else:
                doodle_dict["vel_y"] = JUMP_VELOCITY
                if p["type"] == "brown":
                    p["active"] = False

            break  # Un seul rebond par appel
# =====================================================================


# ======================== PARTIE 3.3 — CORRIGÉ ========================
def scroll_camera():
    """
    Fait défiler le monde lorsque le Doodle dépasse CAMERA_SCROLL_THRESHOLD.
    Met à jour le score et maintient les plateformes visibles.
    """
    if doodle_dict["y"] < CAMERA_SCROLL_THRESHOLD:
        shift_y = CAMERA_SCROLL_THRESHOLD - doodle_dict["y"]
        doodle_dict["y"] = CAMERA_SCROLL_THRESHOLD

        for p in PLATFORMS:
            p["y"] += shift_y

        doodle_dict["score"] += shift_y
        if doodle_dict["score"] > doodle_dict["high_score"]:
            doodle_dict["high_score"] = doodle_dict["score"]

        # Modifier le contenu de la liste existante afin de conserver les
        # références partagées vers PLATFORMS dans les autres modules.
        PLATFORMS[:] = [p for p in PLATFORMS if p["y"] < SCREEN_HEIGHT]

        generate_new_platforms()
# =====================================================================


# ======================== PARTIE 3.4 — CORRIGÉ ========================
def generate_new_platforms():
    """
    Génère de nouvelles plateformes au-dessus du haut de l'écran pour maintenir
    un flux continu lorsque la caméra défile.
    """
    if not PLATFORMS:
        return

    highest_y = min(p["y"] for p in PLATFORMS)

    while highest_y > 0:
        new_y = highest_y - random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
        new_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        platform_type = choose_platform_type(0.55, 0.20, 0.13)

        PLATFORMS.append(create_platform(new_x, new_y, platform_type))
        highest_y = new_y
# =====================================================================


def check_game_over():
    """
    Vérifie si le Doodle tombe sous le bas de l'écran.
    Si oui, réduit les vies.
    Retourne True si la partie est terminée.
    """
    if doodle_dict["y"] > SCREEN_HEIGHT:
        doodle_dict["lives"] -= 1
        return True
    return False


def restart_game():
    """
    Réinitialise la partie : position du Doodle, vitesse, score et plateformes.
    """
    doodle_dict["x"] = DOODLE_START_X
    doodle_dict["y"] = DOODLE_START_Y
    doodle_dict["vel_y"] = 0.0
    doodle_dict["direction"] = "right"
    doodle_dict["image"] = doodle_right_img
    doodle_dict["score"] = 0
    doodle_dict["lives"] = LIVES

    generate_initial_platforms()


def rects_collide(r1, r2):
    """
    Vérifie si deux rectangles (x, y, largeur, hauteur) se chevauchent.
    Cette fonction est fournie et ne doit pas être modifiée.
    """
    return not (
        r1[0] + r1[2] <= r2[0] or r1[0] >= r2[0] + r2[2] or
        r1[1] + r1[3] <= r2[1] or r1[1] >= r2[1] + r2[3]
    )

