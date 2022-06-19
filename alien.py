import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, main_game):
        """初始化外星人并设置起始位置"""
        super().__init__()
        self.screen = main_game.screen
        self.settings = main_game.settings

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load(self.settings.alien_image_path)
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
