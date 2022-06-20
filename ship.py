import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self, main_class):
        """初始化飞船并设置其初始位置"""
        self.screen = main_class.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = main_class.settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(main_class.settings.ship_image_path)
        self.rect = self.image.get_rect()

        # 对于每膄新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed

    def center_ship(self):
        """让飞船在屏幕底端居中"""
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
