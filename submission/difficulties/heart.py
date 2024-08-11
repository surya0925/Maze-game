import pygame

class Heart(pygame.sprite.Sprite):
    IMAGE_WIDTH = 32  # Define the width of the heart image

    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.rect = self.image.get_rect(topleft=position)

class Lives:
    @staticmethod
    def show_lives(screen, lives):
        heart_positions = [(screen.get_width() - (i + 1) * (Heart.IMAGE_WIDTH + 40)-30, 10) for i in range(3)]

        # Create a sprite group for hearts
        heart_group = pygame.sprite.Group()

        # Create heart sprites and add them to the group
        for i, pos in enumerate(heart_positions):
            if i < lives:
                heart = Heart("images/heart.png", pos)
                heart_group.add(heart)

        # Draw the hearts
        heart_group.draw(screen)
