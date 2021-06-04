import math
import json
import pygame


# classe qui va contenir le mécanisme des animations
class AnimateSprite(pygame.sprite.Sprite):

    # definir les choses à faire à la création de l'entité
    def __init__(self, sprite_name, size=(200, 200)):
        super().__init__()
        self.size = size
        self.image = pygame.image.load(f'./assets/{sprite_name}.png')
        self.image = pygame.transform.scale(self.image, size)
        self.current_image = 0  # commencer à l'image 0
        self.images = animations.get(sprite_name)
        self.animation = False

    # définir une méthode pour animer le sprite
    def animate(self, loop=False):
        # verifier si l'animation est active
        if self.animation:
            # passer à l'image suivante
            self.current_image += math.floor(1)

            # vérifier si on a atteint la fin
            if self.current_image >= len(self.images):
                # remettre au départ
                self.current_image = 0

                # verfifier si l'animation n'est pas en mode boucle
                if loop is False:
                    # désactivation de l'animation
                    self.animation = False

            # modifier l'image précédente par la suivant
            self.image = self.images[self.current_image]
            self.image = pygame.transform.scale(self.image, self.size)

    # définir une méthode pour démarrer l'animaion
    def start_animation(self):
        self.animation = True


# fonction pour charger les images d'un sprite
def load_animation_images(sprite_name):
    # charger les images de ce sprite dans le dossier
    images = []
    # récupérer les chemin du dossier pour ce sprite
    path = f"./assets/{sprite_name}/{sprite_name}"

    # Boucler sur chaque image dans ce dossier
    for num in range(1, 25):
        image_path = path + str(num) + '.png'
        images.append(pygame.image.load(image_path))

    return images


# definir un dict qui va contenir les images chargées de chaques images
# mummy -> [...mummy1.png, ...mummy2.png, ...]
animations = {
    'mummy': load_animation_images('mummy'),
    'alien': load_animation_images('alien'),
    'player': load_animation_images('player')
}
