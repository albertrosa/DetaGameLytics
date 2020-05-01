from deta.lib import app
from highscore import Highscore
from deta.lib.responses import JSON, HTML

@app.lib.http("/register/", methods=["POST"])
def post_register_new_game(event):
    email = event.json.get("email")
    key = event.json.get("key")
    game_title = event.json.get("game_title")

    # here we create a new db entry if one doesn't exist per game and password
    # set current limit to 2 games per email
    game_key, message = Highscore.create_game(email, key, game_title)

    if game_key:
        return JSON({
            "success": True,
            "game_key": game_key
        })
    else:
        return JSON({
            "success": False,
            "message": message
        })


@app.lib.http("/recover/key/", methods=["POST"])
def post_register_new_game(event):
    email = event.json.get("email")
    game_title = event.json.get("game_title")

    game_key, message = Highscore.recover_key(email, game_title)

    if game_key:
        return JSON({
            "success": True,
            "game_key": game_key
        })
    else:
        return JSON({
            "success": False,
            "message": message
        })


@app.lib.http("/player/exists/", methods=['POST'])
def add_high_score(event):
    game_key = event.json.get("key")
    player_name = event.json.get("player_name")

    return JSON({
        "success": True,
        "player_exist": Highscore.player_exist(player_name, game_key)
    })


@app.lib.http("/addScore/", methods=['POST'])
def add_high_score(event):
    game_key = event.json.get("key")  ## this is unique per game
    player_name = event.json.get("player_name")
    score = event.json.get("score")

    # here we match the key/id
    added, message = Highscore.add_score(player_name, game_key, score)

    if added:
        return JSON({
            "success": True,
            "message": "Added High Score"
        })
    else:
        return JSON({
            "success": False,
            "message": message
        })


@app.lib.http("/game/highscores/alltime/", methods=['POST'])
def get_ranked_all_time_high_scores(event):
    game_key = event.json.get("key")
    return JSON({"success": True, "highscores": Highscore.get_ranked_game_scores(game_key)})


@app.lib.http("/player/highscore/", methods=['POST'])
def get_player_high_score(event):
    game_key = event.json.get("key")
    player_name = event.json.get("player_name")
    return JSON({"success": True, "highscores": Highscore.get_player_score(player_name, game_key)})


@app.lib.http("/", methods=["GET"])
def get_handler(event):
    name = event.params.get("name")
    return HTML("<html><body><h1>WIP</h1></body></html>")

