import os

import pygame
import math
import json

pygame.init()

from packages.game import Game

# definir une clock
clock = pygame.time.Clock()
FPS = 120

# générer la fenetre de notre jeu
pygame.display.set_caption("comet fall Game")
screen = pygame.display.set_mode((1080, 720))
screen_rect = screen.get_rect()

# Chargement de l'arrière plan du jeu
background = pygame.image.load('assets/bg.jpg')

# importer la bannière
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

# importer le bouton de lancement
play_btn = pygame.image.load('assets/button.png')
play_btn = pygame.transform.scale(play_btn, (400, 150))
play_btn_rect = play_btn.get_rect()
play_btn_rect.x = math.ceil(screen.get_width() / 3.33)
play_btn_rect.y = math.ceil(screen.get_height() / 2)

# création ou chargement de la liste de score
try:
    scores = json.load(open('scores.json', 'r'))
except (FileNotFoundError, json.decoder.JSONDecodeError):
    if os.path.isfile('scores.json'):
        os.rename('scores.json', 'scores.json.bak')

    scores = {
        'Joueur': 0,
        'Meilleur score': 0,
        'Tué': 0,
        'Vagues': 1
    }
    json.dump(scores, open('scores.json', 'w'), indent=4, sort_keys=True)

# Chargement du joueur
game = Game()

running = True

# boucle tant que cette condition est vraie
while running:

    # Application de l'arrière plan du jeu
    screen.blit(background, (0, -200))

    # vérifier si notre jeu a commencé
    if game.is_playing:
        # declencher les instructions de la partie
        game.update(screen)
    # vérifier si le jeu n'a pas commencé
    else:
        # Ajouter l'écran de bvn
        screen.blit(play_btn, play_btn_rect)
        screen.blit(banner, banner_rect)

    # Mettre à jour la fenêtre
    pygame.display.flip()

    # si le joueur ferme cette fenetre
    for event in pygame.event.get():
        # que l'evenement est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # Détercter si le joueur lâche une touche du clavier
        elif event.type == pygame.KEYDOWN:
            # La touche appuyé
            game.pressed[event.key] = True

            # detecter si la touche espace est enclenchée pour le projectile
            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            # Verifier pour savoir si la souris a été appuyé au niveau du bouton
            if game.is_playing:
                if event.button == 4 or event.button == 5:
                    pass

                elif screen_rect.collidepoint(event.pos):
                    # jouer le son
                    game.sound_manager.play('click')
                    # lancer le projectile
                    game.player.launch_projectile()

            elif play_btn_rect.collidepoint(event.pos):
                # jouer le son
                game.sound_manager.play('click')
                # lancer le jeu
                game.start()



    # fixer le nombre de FPS
    clock.tick(FPS)
