import random

import pygame
from packages.projectile import Projectile
from packages import animation


class Player(animation.AnimateSprite):

    def __init__(self, game):
        super().__init__('player')
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.velocity = 5
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def add_health(self, amount):
        if self.health + amount > self.max_health:
            # ajoute des points de vie
            self.health == self.max_health
        else:
            self.health += amount

    def damage(self, amount):
        if self.health - amount > amount:
            # infliger les dégats
            self.health -= amount

        # vérifier si ses PV ne sont pas à 0
        else:
            # Game over
            self.game.game_over()

    def launch_projectile(self):
        # créer une nouvelle instance de la classe
        self.all_projectiles.add(Projectile(self))
        # démarrer l'animation
        self.start_animation()
        # jouer le son
        self.game.sound_manager.play('tir')

    def move_right(self):
        # Si le joueur n'est pas en collision
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def update_animation(self):
        self.animate()

    def update_health_bar(self, surface):
        # dessiner notre barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 50, self.rect.y + 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 50, self.rect.y + 20, self.health, 5])
