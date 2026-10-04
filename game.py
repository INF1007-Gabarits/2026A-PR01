# ======================== game.py ========================

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_VELOCITY, SPRING_JUMP_VELOCITY,
    DOODLE_SPEED, DOODLE_WIDTH, DOODLE_HEIGHT, PLATFORM_WIDTH,
    MIN_PLATFORM_GAP, MAX_PLATFORM_GAP, CAMERA_SCROLL_THRESHOLD,
    PLATFORMS, doodle_dict, DOODLE_START_X, DOODLE_START_Y, LIVES, MOVING_PLATFORM_SPEED
)
from platforms import create_platform, choose_platform_type
from doodle import doodle_left_img, doodle_right_img
from window import generate_initial_platforms


# ======================== PARTIE 3.1 ========================
def apply_gravity(): #JOUDKATBE
    """
    Applique la gravité au Doodle en augmentant progressivement sa vitesse verticale (vel_y).
    Met à jour la position verticale (y) du Doodle.
    """
    doodle_dict["vel_y"] += GRAVITY          # 1. la gravité change la vitesse
    doodle_dict["y"] += doodle_dict["vel_y"]  # 2. la vitesse change la position
    # TODO : Mettez à jour la vitesse verticale puis la position verticale
    # du Doodle à partir de GRAVITY.
    # vel_y = (JUMP_VELOCITY ** 2) + 2(GRAVITY)

    return

# ===========================================================


# ======================== PARTIE 1.2 ========================
def move_doodle(): #ALEX
    """
    Gère le déplacement horizontal du Doodle selon les touches pressées (Flèches ou A/D).
    Implémente le passage fluide d'un côté de l'écran à l'autre (Screen Wrap).
    """
    keys = pygame.key.get_pressed()

    # TODO : Gérez les déplacements gauche/droite et mettez à jour
    # simultanément la direction et l'image du Doodle.

    if keys[pygame.K_LEFT]: 
        doodle_dict.update({"direction": "left"})
        doodle_dict.update({"image": doodle_left_img})
        doodle_dict.update({"x": doodle_dict.get("x") - DOODLE_SPEED})

    if keys[pygame.K_RIGHT]: 
            doodle_dict.update({"direction": "right"})
            doodle_dict.update({"image": doodle_right_img})
            doodle_dict.update({"x": doodle_dict.get("x") + DOODLE_SPEED})
        

    # TODO : Implémentez le Screen Wrap pour qu'une partie du Doodle puisse
    # sortir d'un côté avant de réapparaître de l'autre.
    # N'utilisez pas de dimensions numériques écrites directement.

    if doodle_dict.get("x") > SCREEN_WIDTH - DOODLE_WIDTH // 2:
        doodle_dict.update({"x": -DOODLE_WIDTH //2 })
    elif (doodle_dict.get("x") < -DOODLE_WIDTH // 2):
        doodle_dict.update({"x": SCREEN_WIDTH - DOODLE_WIDTH // 2})

    return

# ===========================================================


# ======================== PARTIE 2.3 ========================
def move_platforms(): #JOUDKATBE
    """
    Déplace horizontalement les plateformes mobiles ("blue").
    Fait rebondir les plateformes lorsqu'elles atteignent les bords de la fenêtre.
    """
    for platform in PLATFORMS:  #check si la platform est bleu
        if platform["type"] == "blue":
            platform["x"]+= platform["vx"] #platform["vx"] = 3 
            if (platform["x"]+platform["width"])>SCREEN_WIDTH:
                platform["vx"]= -platform["vx"]
            if platform["x"]<=0:
                platform["vx"]= abs(platform["vx"]) # si sa touche lextremiter gauche, la vitesse devien positive
        #platforme platform["vx"]
    # TODO : Parcourez les plateformes et gérez le déplacement des plateformes
    # bleues encore actives. Elles doivent rester dans la fenêtre en inversant
    # leur vitesse lorsqu'elles atteignent un bord.

    

    return

# ===========================================================


# ======================== PARTIE 3.2 ========================
def check_platform_collisions():
    """
    Détecte si le Doodle atterrit sur une plateforme.
    Le rebond ne se produit QUE lorsque le Doodle descend (vel_y > 0)
    et qu'il arrive sur le dessus d'une plateforme.
    """
    # TODO : Implémentez la détection d'un atterrissage.
    #
    # Contraintes :
    # - aucun rebond pendant la montée ;
    # - ignorer les plateformes inactives ;
    # - utiliser rects_collide(...) pour le chevauchement des rectangles ;
    # - un simple chevauchement ne suffit pas : le Doodle doit arriver par
    #   le dessus de la plateforme. Pour le vérifier, comparez la position
    #   actuelle de ses pieds à leur position approximative à l'image
    #   précédente à l'aide de vel_y. Une tolérance de 14 pixels est permise ;
    # - spring : SPRING_JUMP_VELOCITY ;
    # - brown : JUMP_VELOCITY puis désactivation de la plateforme ;
    # - green/blue : JUMP_VELOCITY.

    if doodle_dict["vel_y"] > 0:
        for platform in PLATFORMS:
            r1 = (doodle_dict["x"], doodle_dict["y"], DOODLE_WIDTH, DOODLE_HEIGHT)
            r2 = (platform["x"], platform["y"], platform["width"], -14)
            
            if (platform["active"] and rects_collide(r1, r2)
                    and not (doodle_dict["y"] == platform["y"])
                    ):

                if platform["type"] in ["green", "blue"]:
                    doodle_dict["vel_y"] = JUMP_VELOCITY
                    doodle_dict["y"] += doodle_dict["vel_y"]
                elif platform["type"] == "spring":
                    doodle_dict["vel_y"] = SPRING_JUMP_VELOCITY
                    doodle_dict["y"] += doodle_dict["vel_y"]
                else:
                    doodle_dict["vel_y"] = JUMP_VELOCITY
                    doodle_dict["y"] += doodle_dict["vel_y"]
                    platform["active"] = False

       

    return

# ===========================================================


# ======================== PARTIE 3.3 ========================
def scroll_camera():# joud Katbe
    """
    Fait défiler le monde lorsque le Doodle dépasse CAMERA_SCROLL_THRESHOLD.
    Met à jour le score et maintient les plateformes visibles.
    """
    if doodle_dict["y"] < CAMERA_SCROLL_THRESHOLD:
        distance = CAMERA_SCROLL_THRESHOLD - doodle_dict["y"]

        
        doodle_dict["y"] = CAMERA_SCROLL_THRESHOLD # 1. Le Doodle reste au seuil

        
        for platform in PLATFORMS: # 2. Les plateformes descendent de la même distance
            platform["y"] += distance

        
        doodle_dict["score"] += distance # 3. Score et meilleur score
        if doodle_dict["score"] > doodle_dict["high_score"]:
            doodle_dict["high_score"] = doodle_dict["score"]


        PLATFORMS[:] = [p for p in PLATFORMS if p["y"] < SCREEN_HEIGHT] # 4. Retirer les plateformes sorties sous l'écran

        
        generate_new_platforms()

    return
    # TODO : Lorsque le Doodle dépasse le seuil de caméra, il doit rester
    # visuellement au seuil pendant que les plateformes sont déplacées vers
    # le bas de la même distance.
    #
    # Le score doit représenter la distance verticale ainsi parcourue et le
    # meilleur score doit être mis à jour. Les plateformes sorties sous
    # l'écran doivent être retirées, puis de nouvelles plateformes générées.

    return

# ===========================================================


# ======================== PARTIE 3.4 ========================
def generate_new_platforms():  # joudkatbe
    """
    Génère de nouvelles plateformes au-dessus du haut de l'écran pour maintenir
    un flux continu lorsque la caméra défile.
    """
    # Point de départ : la plateforme la plus haute (le plus petit y)
    if len(PLATFORMS) == 0:
        plus_haute = SCREEN_HEIGHT
    else:
        plus_haute = min(p["y"] for p in PLATFORMS)

    # Ajouter des plateformes tant que le haut de l'écran n'est pas rempli
    while plus_haute > 0:
        plus_haute -= random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
        x = random.uniform(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        type_plateforme = choose_platform_type(0.55, 0.20, 0.13)
        PLATFORMS.append(create_platform(x, plus_haute, type_plateforme))

    # TODO : Complétez cette fonction en vous inspirant de la logique de
    # génération initiale, sans la recopier inutilement.
    #
    # Vous devrez partir de la plateforme actuellement la plus haute et
    # continuer à ajouter des plateformes tant que nécessaire. Utilisez
    # choose_platform_type(...) avec les probabilités indiquées dans le README.

    return

# ===========================================================


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
