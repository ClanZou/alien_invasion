import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""

    def __init__(self, main_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.settings = main_game.settings

        # 在(0,0)出创建一个表示子弹的矩形，再设置正确的位置
        """
        这里最好命名rect，因为sprite里对这个属性有设置
        有些方法也要求必须存在rect属性，比如pygame.sprite.draw
        """
        self.rect = pygame.Rect(self.settings.bullet_width_and_height)

        """
        self.midtop一旦赋值
        其它self.midright、self.midleft、self.midbootm的值也会同时改变
        只能推测pygame.Rect内部设定了相关运算
        """
        self.rect.midtop = main_game.ship.rect.midtop

        self.shooting_flag = False
        self.shooting_timing = False

        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹的rect的位置
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
