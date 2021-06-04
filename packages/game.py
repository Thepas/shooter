import json
import math

from packages.comet_event import CometFallEvent
from packages.monsters import *
from packages.player import Player
from packages.sounds import SoundManager


class Game:

    def __init__(self):
        # definir si notre jeu a commencé ou non
        self.is_playing = False
        # Générer le joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        # générer l'event
        self.comet_event = CometFallEvent(self)
        # groupe de monstres
        self.all_monsters = pygame.sprite.Group()
        # gerer le son
        self.sound_manager = SoundManager()
        self.pressed = {}
        # Récupérer les scores
        self.scores = json.load(open('scores.json', 'r'))
        #####
        self.score = 0
        self.kill = 0
        self.vague = 1
        # afficher un texte
        self.myfont = pygame.font.Font("./assets/PottaOne.ttf", 25)

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def game_over(self):
        # revenir au menu: retirer les monstres, remettre le joueur à 100 de vie, jeu en attente
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.save_score()
        self.score = 0
        self.kill = 0
        self.vague = 1
        self.sound_manager.play('game_over')

    def save_score(self):
        if self.score > self.scores['Meilleur score']:
            self.scores['Meilleur score'] = self.score

        if self.kill > self.scores['Tué']:
            self.scores['Tué'] = self.kill

        if self.vague > self.scores['Vagues']:
            self.scores['Vagues'] = self.vague

        json.dump(self.scores, open('scores.json', 'w'), indent=4, sort_keys=True)

    def start(self):
        self.is_playing = True
        elm = [Mummy, Mummy, Mummy, Alien]
        for i in range(0, random.randint(3, 5)):
            self.spawn_monster(random.choice(elm))

    def spawn_monster(self, monster_class):
        self.all_monsters.add(monster_class.__call__(self))

    def update(self, screen):
        # Application de l'image du joueur
        screen.blit(self.player.image, self.player.rect)

        # Application du score
        self.score_display = self.myfont.render(f"Score: {self.score}", 1, (255, 255, 0))
        screen.blit(self.score_display, (20, 20))

        self.kill_display = self.myfont.render(f"Tué: {self.kill}", 1, (255, 255, 0))
        screen.blit(self.kill_display, (20, 50))

        # Vagues en cours

        self.wave_display = self.myfont.render(f"Vagues: {self.vague}", 1, (255, 255, 0))
        screen.blit(self.wave_display, (math.ceil(screen.get_width() / 2), math.ceil(screen.get_height() / 6)))

        # Affichage du Highscore
        self.Highscore_display = self.myfont.render(f"Meilleur score: {self.scores['Meilleur score']}", 1,
                                                    (255, 255, 0))
        screen.blit(self.Highscore_display, (20, 80))

        self.Highkill_display = self.myfont.render(f"Record tué: {self.scores['Tué']}", 1, (255, 255, 0))
        screen.blit(self.Highkill_display, (20, 110))

        self.HighWaves_display = self.myfont.render(f"Record vagues: {self.scores['Vagues']}", 1, (255, 255, 0))
        screen.blit(self.HighWaves_display, (20, 140))

        # Actualiser la barre de vie du joueur
        self.player.update_health_bar(screen)

        # Actualiser la barre de l'event
        self.comet_event.update_bar(screen)

        # Actualiser l'animation du joueur
        self.player.update_animation()

        # recupérer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()

        # récupérer les monstres de notre jeu
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()
        # récupérer les comtes de notre jeu
        for comet in self.comet_event.all_comets:
            comet.fall()

        # appliquer l'ensemble des projectiles
        self.player.all_projectiles.draw(screen)

        # Appliquer l'ensemble des images du groupe de monstres
        self.all_monsters.draw(screen)

        # appliquer l'ensemble des cometes
        self.comet_event.all_comets.draw(screen)

        # Verfifier la direction voulue
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

    def update_score(self, point=10):
        self.score += point
        self.kill += 1
