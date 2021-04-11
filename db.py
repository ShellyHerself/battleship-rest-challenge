# I like to avoid import *, but we need a lot of things imported from peewee
# And we're only using them here
# Using playhouse extensions for JSON support
from playhouse.sqlite_ext import *

import game_logic

db = SqliteExtDatabase('battleship.db', pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def getById(cls, id):
        '''Gets a table entry by id'''
        try:
            entry = cls.select().where(cls.id == id).get()
            return entry
        except DoesNotExist:
            return None

class DbBattleShipGame(BaseModel):
    id                  = AutoField()
    player_boards       = JSONField(default=[])
    player_last_turns   = JSONField(default=[None, None])
    turn_player         = IntegerField(null=True)
    status              = TextField(null=False, default="PRE_GAME")

    def toObject(self):
        '''Converts a game database object to an active BattleShipGame'''
        game = game_logic.BattleShipGame()
        game.id = self.id

        # Convert boards from their json repr
        for json_board in self.player_boards:
            board = game_logic.BattleShipPlayerBoard()
            board.ship_squares = json_board['ship_squares']
            game.player_boards.append(board)

        game.player_last_turns = self.player_last_turns
        game.turn_player = self.turn_player
        game.game_status = self.status

        return game

    def fromObject(self, object):
        '''Writes the data from a BattleShipGame to the given database entry'''
        json_boards = []
        for board in game.player_boards:
            json_board = {}
            json_board['ship_squares'] = board.ship_squares
            json_boards.append(json_board)

        self.player_boards = json_boards
        self.player_last_turns = game.player_last_turns
        self.turn_player = game.turn_player
        self.status = game.game_status

def wipeDatabase():
    DbBattleShipGame.delete().execute()

db.connect()
db.create_tables([DbBattleShipGame])
