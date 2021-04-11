import json
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

import db
import game_logic

app = Flask(__name__)
api = Api(app)

def abortWithReason(error_code, text):
    '''Sends the user a given error code with the given message'''
    abort(error_code, message={"reason": text})

def battleShipGameToListedGame(game):
    '''Converts a given game to the JSON specification in our API'''
    listed_game = {
        'id': game.id,
        'status': game.game_status,
        'player_count': len(game.player_boards),
        'player_last_moves': game.player_last_turns,
        'turn_player': game.turn_player
    }
    player_healths = []
    for board in game.player_boards:
        player_healths.append(board.getTotalHealth())

    listed_game['player_healths'] = player_healths

    return listed_game

def getDbGameOrAbort(game_id):
    '''Tries to get a game'''
    game = db.DbBattleShipGame.getById(game_id)
    if game is None:
        abortWithReason(404, "Game with id: {} doesn't exist".format(game_id))
    return game

def createDbGameOrAbort():
    '''Creates a game'''
    try:
        game = db.DbBattleShipGame.create(status="PRE_GAME")
        game.save()
        if game is None:
            abortWithReason(500, "Couldn't create game")
    except Exception:
        # TODO Log exception
        abortWithReason(500, "Couldn't create game")

    return game

game_move_parser = reqparse.RequestParser()
game_move_parser.add_argument('player_id', required=True)
game_move_parser.add_argument('move', required=True)

class GameMove(Resource):
    def post(self, game_id):
        args = game_move_parser.parse_args()
        try:
            move = json.loads(args['move'])
            x = move['x']
            y = move['y']
        except Exception:
            abortWithReason(
                400, "Move field in request requires both an 'x' and a 'y' field as integers")
        # Retrieve the game in the database
        game = getDbGameOrAbort(game_id)
        try:
            # Create our game logic object
            game_obj = game.toObject()
            # Try to join our player into the game
            hit = game_obj.makeMove(int(args['player_id']), x, y)
            # serialize the data from our game object back to the database
            game.fromObject(game_obj)
            game.save()
            return {'hit': hit}, 200
        except game_logic.PlayerError as e:
            abortWithReason(400, e)

        # This line should be unreachable. But just in case
        abortWithReason(500, "Unreachable condition")

class Game(Resource):
    def get(self, game_id):
        '''Gets the current status of a game'''
        return battleShipGameToListedGame(getDbGameOrAbort(game_id).toObject()), 200

    def post(self, game_id):
        # Retrieve the game in the database
        game = getDbGameOrAbort(game_id)
        try:
            # Create our game logic object
            game_obj = game.toObject()
            # Try to join our player into the game
            player_id = game_obj.joinPlayer()
            game_obj.startIfEnoughPlayers()
            # serialize the data from our game object back to the database
            game.fromObject(game_obj)
            game.save()
        except game_logic.PlayerError as e:
            print(e)
            abortWithReason(400, e)
        return {
            'joined_game_id': game.id,
            'player_id': player_id
        }, 200

class GamesList(Resource):
    def get(self):
        '''Gets the status of all games'''
        response = []
        games = db.DbBattleShipGame.select()
        for game in games:
            response.append(battleShipGameToListedGame(game.toObject()))

        return response

    def post(self):
        '''Tries to create a game and joins the creating general into it'''
        # Create the game in the database
        game = createDbGameOrAbort()
        try:
            # Create our game logic object
            game_obj = game_logic.BattleShipGame()
            # Try to join our player into the game
            player_id = game_obj.joinPlayer()
            game_obj.startIfEnoughPlayers()
            # serialize the data from our game object back to the database
            game.fromObject(game_obj)
            game.save()
        except game_logic.PlayerError as e:
            abortWithReason(400, e)
        return {
            'joined_game_id': game.id,
            'player_id': player_id
        }, 201

api.add_resource(GamesList, '/games')
api.add_resource(Game, '/games/<game_id>')
api.add_resource(GameMove, '/games/<game_id>/fire')

if __name__ == '__main__':
    app.run(debug=True)
