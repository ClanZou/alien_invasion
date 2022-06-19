import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_width_and_height)
        pygame.display.set_caption(self.settings.screen_caption)

        self.ship = Ship(self)

        """
        sprite内置了update方法，所以在run_game可以直接调用
        如果不使用sprite.Group()，也可以自创一个[]空列表
        然后不能在self.bullets.update，要在_update_screen的for读取bullet时调用update
        """
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除子弹"""
        # 更新子弹位置
        self.bullets.update()

        """
        使用for循环遍历列表（或Pygame编组）时，Python要求该列表的长度在整个循环中保持不变
        因为不能从for循环遍历的列表或编组中删除元素，所以必须遍历编组的副本
        """
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.bullet_rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
