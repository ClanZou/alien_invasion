class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, main_game):
        """初始化统计信息"""
        self.settings = main_game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ship_life = self.settings.ship_limit
        self.game_active = True
        self.score = 0
