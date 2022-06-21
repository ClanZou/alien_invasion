class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化屏幕设置"""
        # 屏幕设置
        self.screen_width_and_height = (1200, 800)
        self.screen_caption = "Alien Invasion"
        self.bg_color = (230, 230, 230)

        self.ship_image_path = "images/ship.bmp"
        self.ship_speed = 1
        self.ship_limit = 3

        self.bullet_speed = 1
        self.bullet_width_and_height = (0, 0, 3, 15)
        self.bullet_color = (60, 60, 60)

        self.alien_image_path = "images/alien.bmp"
        self.alien_speed = 1
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
