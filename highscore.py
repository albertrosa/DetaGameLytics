from deta.lib import Database
import secrets
import json

db = Database("highscores")


class Player:
    id = None
    name = None
    score = 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Game:
    id = None
    token = None
    email = None
    gameTitle = None
    players = []

    def __init__(self, id, token, email, gameTitle):
        self.id = id
        self.token = token
        self.email = email
        self.gameTitle = gameTitle

    def toJSON(self):
        return {
            "id": self.id,
            "token": self.token,
            "email": self.email,
            "gameTitle": self.gameTitle,
            "players": self.players
        }


class Highscore:

    @staticmethod
    def create_game(email, game_title):
        def generate_game_key():
            token = secrets.token_urlsafe(32)
            try:
                db.get(token)
                return generate_game_key()
            except:
                return token

        id = "%s_%s" % (email, game_title.replace(" ", ""))

        try:
            db.get(id)
            return None, "Token for Game Exists"
        except KeyError:
            token = generate_game_key()
            game = Game(id=id, token=token, email=email, gameTitle=game_title)
            db.put(id, game.toJSON())
            db.put(token, id)

        return token, None

    @staticmethod
    def recover_key(email, game_title):
        id = "%s_%s" % (email, game_title.replace(" ", ""))

        try:
            return db.get(id)['data']['token'], None
        except KeyError:
            return None, "Game Key Does Not Exist"

    @staticmethod
    def player_exist(player_name, key):
        player_game_id = '%s_%s' % (player_name, key)

        try:
            db.get(player_game_id)
            return True
        except KeyError:
            return False

    @staticmethod
    def add_score(player_name, key, score):
        player_game_id = '%s_%s' % (player_name, key)
        db.put(player_game_id, score)

        try:
            gameID = db.get(key)['data']
            game = db.get(gameID)['data']

            if player_game_id not in game['players']:
                game['players'].append(player_game_id)
                db.put(gameID, game)
        except:
            return False, "cannot add player to game"

        return True, None

    @staticmethod
    def get_player_score(player_name, key):
        player_game_id = '%s_%s' % (player_name, key)
        try:
            return db.get(player_game_id)['data']
        except KeyError:
            return 0

    @staticmethod
    def get_players(key):
        try:
            return db.get(key)['data']['players']
        except KeyError:
            return []

    @staticmethod
    def all():
        return db.all()

    @staticmethod
    def clearAll():
        all = db.all()

        for record in all:
            key = record['key']
            db.delete(key)
