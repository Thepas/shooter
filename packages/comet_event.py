import random

import pygame

from packages.comet import Comet


# créer une classe pour gérer cet évenement
from packages.potion import Potion


class CometFallEvent:

    # lors du chargement -> créer un compteur
    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 5
        self.game = game
        self.fall_mode = False

        # définir un groupe de sprite pour stocker nos cometes
        self.all_comets = pygame.sprite.Group()

    def add_percent(self):
        self.percent += (self.percent_speed / 100)

    def attempt_fall(self):
        # la jauge d'event est full chargée
        if self.is_full_loaded() and len(self.game.all_monsters) == 0:
            self.comet_fall()
            self.fall_mode = True  # activer l'event

    def comet_fall(self):
        # boucle pour les valeurs de 1 à 10
        for i in range(1, 16):
            self.all_comets.add(Comet(self))
            if i == random.randint(1, 15):
                self.all_comets.add(Potion(self))

    def is_full_loaded(self):
        return self.percent >= 100

    def reset_percent(self):
        self.percent = 0

    def update_bar(self, surface):
        # ajouter du pourcentage à la bar
        self.add_percent()

        # appel pour essayer de déclencher les comet
        # self.attempt_fall()

        # barre noir (back)
        pygame.draw.rect(surface, (0, 0, 0), [
            0,  # axe des x
            surface.get_height() - 20,  # axe des Y
            surface.get_width(),  # longeur de la fenetre
            10  # epaisseur de la barre
        ])
        # barre rouge (jauge d'event)
        pygame.draw.rect(surface, (187, 11, 11), [
            0,  # axe des x
            surface.get_height() - 20,  # axe des Y
            ((surface.get_width() / 100) * self.percent),  # longeur de la fenetre
            10
        ])
