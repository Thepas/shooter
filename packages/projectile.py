import pygame


# Definir la classe qui va gérer le projectile de notre joueur
class Projectile(pygame.sprite.Sprite):

    # definir le constructeur de la classe
    def __init__(self, player):
        super().__init__()
        self.velocity = 10
        self.player = player
        self.image = pygame.image.load('./assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def move(self):
        self.rect.x += self.velocity
        self.rotate()

        # Verfifier la collision

        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            self.remove()
            monster.damage(self.player.attack)

        # Vérifier si notre projectile n'est plus présent
        if self.rect.x > 1080:
            # Supprimer le projectile (en dehors de l'écran)
            self.remove()

    def remove(self):
        self.player.all_projectiles.remove(self)

    def rotate(self):
        # tourner le projectile
        self.angle += 8
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
