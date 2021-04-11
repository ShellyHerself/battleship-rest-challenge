from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

import db
import game_logic

app = Flask(__name__)
api = Api(app)

def abortWithReason(error_code, text):
    '''Sends the user a given error code with the given message'''
    abort(error_code, message={"reason": text})

class GameMove(Resource):
    def post(self, game_id):
        pass

class Game(Resource):
    def get(self, game_id):
        pass

    def post(self, game_id):
        pass

class GamesList(Resource):
    def get(self):
        pass

    def post(self):
        pass

api.add_resource(GamesList, '/games')
api.add_resource(Game, '/games/<game_id>')
api.add_resource(GameMove, '/games/<game_id>/fire')

if __name__ == '__main__':
    app.run(debug=True)
