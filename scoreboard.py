import pygame.font


class ScoreBoard:
    """显示得分信息的类"""

    def __init__(self, main_game):
        """初始化显示得分涉及的属性"""
        self.screen = main_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = main_game.settings
        self.game_stats = main_game.game_stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.prep_score()

    def prep_score(self):
        """将得分转换为一副渲染的图像"""
        rounded_score = round(self.game_stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)