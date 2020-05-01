class Highscore:

    @staticmethod
    def create_game(email, key, game_title):
        return "keyFed", None

    @staticmethod
    def recover_key(email, game_title):
        return "keyFed", None

    @staticmethod
    def player_exist(player_name, key):
        return True

    @staticmethod
    def add_score(player_name, key, score):
        return True, None

    @staticmethod
    def get_player_score(player_name, key):
        pass

    @staticmethod
    def get_ranked_game_scores(key, start_time=None, end_time=None):
        pass
