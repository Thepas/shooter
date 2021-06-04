import json

import pygame
import random

from packages import animation


# Créer une classe qui va gérer la notion de monstre

class Monster(animation.AnimateSprite):

    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.3
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 540 - offset
        self.loot_amount = 10
        self.start_animation()

    def damage(self, amount):
        # infliger les dégats
        self.health -= amount

        # vérifier si ses PV ne sont pas à 0
        if self.health <= 0:
            # Réapparaitre comme un nouveau monstre
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, self.default_speed)
            self.health = self.max_health
            # ajouter le nombre de points
            self.game.update_score(self.loot_amount)

            # si la barre d'event est full
            if self.game.comet_event.is_full_loaded():
                # retirer du jeu
                self.game.all_monsters.remove(self)

                # on appel la methode pour essayer de déclencher la pluie de cometes
                self.game.comet_event.attempt_fall()

    def forward(self):
        # le déplacement ne se fait que si ya pa collision
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        # Si ya collision le joueur reçoit des dégats
        else:
            # Infliger des dégats (au joueur)
            self.game.player.damage(self.attack)

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1, 4)

    def set_loot_amount(self, amount):
        self.loot_amount = amount

    def update_animation(self):
        self.animate(loop=True)

    def update_health_bar(self, surface):

        # dessiner notre barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 10, self.rect.y - 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 10, self.rect.y - 20, self.health, 5])


# définir une classe pour la momie
class Mummy(Monster):

    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.set_speed(3)
        self.set_loot_amount(20)


# définir une classe pour l'alien
class Alien(Monster):

    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), offset=120)
        self.health = 250
        self.max_health = 250
        self.attack = 0.8
        self.set_speed(1)
        self.set_loot_amount(80)
