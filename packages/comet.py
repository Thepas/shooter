import pygame
import random


# une classe pour gérer cette comete
class Comet(pygame.sprite.Sprite):

    def __init__(self, comet_event):
        super().__init__()
        # definir l'image de la comete
        self.image = pygame.image.load('./assets/comet.png')
        self.rect = self.image.get_rect()
        self.velocity = random.randint(3, 5)
        self.rect.x = random.randint(15, 800)
        self.rect.y = -random.randint(0, 800)
        self.comet_event = comet_event

    def fall(self):
        self.rect.y += self.velocity

        # ne tombe pas sur le sol
        if self.rect.y >= 500:
            self.remove()

            # si il n'y a plus de boule de feu
            if len(self.comet_event.all_comets) == 0:
                # remettre la jauge à 0
                self.comet_event.reset_percent()
                self.comet_event.fall_mode = False
                self.comet_event.game.vague += 1

        # verifier si la boule de feu touche le joueur
        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            self.remove()
            # subir des dégats
            self.comet_event.game.player.damage(20)

    def remove(self):
        # retirer la boule
        self.comet_event.all_comets.remove(self)
        # jouer le son
        self.comet_event.game.sound_manager.play('meteorite')

        # vérifier si il reste des cometes
        if len(self.comet_event.all_comets) == 0:
            # remettre la barre à 0
            self.comet_event.reset_percent()
            # apparaitre les 2 premiers monstre
            self.comet_event.game.start()
