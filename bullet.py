import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""

    def __init__(self, main_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = main_game.screen
        self.settings = main_game.settings
        self.bullet_color = self.settings.bullet_color

        # 在(0,0)出创建一个表示子弹的矩形，再设置正确的位置
        self.bullet_rect = pygame.Rect(self.settings.bullet_width_and_height)

        """
        self.midtop一旦赋值
        其它self.midright、self.midleft、self.midbootm的值也会同时改变
        只能推测pygame.Rect内部设定了相关运算
        """
        self.bullet_rect.midtop = main_game.ship.image_rect.midtop

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹的rect的位置
        self.bullet_rect.y -= self.settings.bullet_speed

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.bullet_color, self.bullet_rect)
