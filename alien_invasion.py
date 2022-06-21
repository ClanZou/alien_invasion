import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_width_and_height)
        pygame.display.set_caption(self.settings.screen_caption)

        self.game_stats = GameStats(self)

        self.ship = Ship(self)

        """
        sprite内置了update方法，所以在run_game可以直接调用
        如果不使用sprite.Group()，也可以自创一个[]空列表
        然后不能在self.bullets.update，要在_update_screen的for读取bullet时调用update
        """
        self.bullets = pygame.sprite.Group()
        self.bullet = Bullet(self)

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.game_stats.game_active:
                self.ship.update()
                self._fire_bullet()
                self._update_bullets()
                self._update_aliens()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.bullet.shooting_flag = True
            self.bullet.shooting_timing = True
        elif event.key == pygame.K_p:
            self._check_play_button((self.play_button.rect.x, self.play_button.rect.y))

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self.bullet.shooting_flag = False
            self.bullet.shooting_timing = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if self.bullet.shooting_flag:
            """
            当shooting_timing为False时，什么都不做并退出方法
            在按下space键时会为True，所以可以发射第一个bullet
            之后当符合update_bullet循环中的判断条件时，才能发射第二个bullet
            直到松开space，重新开始while主循环
            """
            if not self.bullet.shooting_timing:
                return
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除子弹"""
        # 更新子弹位置
        """
        可以在update()中设置shooting_timing默认为False
        但是因为只能用一个实例bullet而不是bullets来判断是否连续发射子弹
        所以如果在update()中设置了，那在这里还需要执行一次self.bullet.update()
        也可以在主程序创建一个新变量而不使用Bullet类中的属性，但这样不符合面向对象原则
        """
        self.bullets.update()

        """
        使用for循环遍历列表（或Pygame编组）时，Python要求该列表的长度在整个循环中保持不变
        因为不能从for循环遍历的列表或编组中删除元素，所以必须遍历编组的副本
        """
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            """
            使用一个实例bullet，通过设置它的shooting_timing判断是否连续发射子弹
            当bullet的y轴超过8个bullet高度，设置shooting_timing为True
            其它情况都为False
            """
            if bullet.rect.y == self.ship.rect.y - 8 * bullet.rect.height:
                self.bullet.shooting_timing = True
            else:
                self.bullet.shooting_timing = False

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """
        当有子弹和外星人的rect重叠，groupcollide() 在它返回的字典中添加一个键值对
        两个实参True让Pygame删除发生碰撞的子弹和外星人
        """

        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # 创造一群新外星人
        if not self.aliens:
            self._create_fleet()
            self.settings.increase_speed()

    def _create_fleet(self):
        """创建外星人群"""
        # 创建第一行外星人
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        # 留余左右各一个空位
        available_space_x = self.settings.screen_width_and_height[0] - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)

        # 留余上下个一个空位，并额外在ship前留余一个空位，排除ship所在行被计算进去
        available_space_y = self.settings.screen_width_and_height[1] - 3 * alien_height - self.ship.rect.height
        # 这里结果为4.9，所以只有4行
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其放在当前行"""
        alien = Alien(self)
        """这里必须要先赋值给alien.x，因为alien.update()中alien.x+=是浮点运算结果一定为浮点值"""
        alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检测是否有外星人到达屏幕底端
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船被外星人撞到"""

        if self.game_stats.ship_life > 0:
            # 将ships_left减1
            self.game_stats.ship_life -= 1

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_play_button(self, mouse_pos):
        """在玩家单击play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_stats.game_active:
            # 重置游戏统计信息
            self.game_stats.reset_stats()
            self.game_stats.game_active = True

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            pygame.draw.rect(self.screen, self.settings.bullet_color, bullet.rect)
        self.aliens.draw(self.screen)

        if not self.game_stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
