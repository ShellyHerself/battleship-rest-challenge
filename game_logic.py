# These are hardcoded due to time constraints
HARDCODED_SHIP_PLACEMENTS = (
    {'x':3, 'y':4, 'allignment': 'x', 'length': 5},
    {'x':3, 'y':6, 'allignment': 'x', 'length': 4},
    {'x':5, 'y':6, 'allignment': 'y', 'length': 3},
    {'x':7, 'y':6, 'allignment': 'y', 'length': 3},
    {'x':8, 'y':9, 'allignment': 'y', 'length': 2},
)

class PlayerError(Exception):
    pass

class BattleShipPlayerBoard:
    ship_squares = []

    def addShip(self, x, y, allignment, length):
        new_squares = []
        if (allignment == 'x'):
            for i in range(length):
                new_squares.append({'x':x+1, 'y':y})
        elif (allignment == 'y'):
            for i in range(length):
                new_squares.append({'x':x, 'y':y+1})
        else:
            raise PlayerError("Allignment for ship placement needs to be either 'x' or 'y'")

        for square in new_squares:
            if self.ship_squares.count(square) > 0:
                raise PlayerError("Placed ship overlaps with another ship")
            if square['x'] < 0 or square['x'] >= 10 or square['y'] < 0 or square['y'] >= 10:
                raise PlayerError("Ship placement is out of bounds")

        self.ship_squares.extend(new_squares)

    def checkHit(self, x, y):
        '''
        Checks if there is a hit at these coordinates and removes any ship squares there.
        Returns if there was a hit
        '''
        square = {'x':x, 'y':y}

        if square['x'] < 0 or square['x'] >= 10 or square['y'] < 0 or square['y'] >= 10:
            raise PlayerError("Tried to make a move that is out of bounds")

        hit_count = self.ship_squares.count(square)
        for i in range(hit_count):
            self.ship_squares.remove(square)

        return hit_count > 0

    def getTotalHealth(self):
        return len(ship_squares)

class BattleShipGame:
    id = None
    player_boards = []
    # Allows for clients to check what their opponent's last move was
    player_last_turns = [None, None]
    turn_player = None
    # TODO, All these statuses should be defined as some sort of an enum
    game_status = "PRE_GAME"

    @staticmethod
    def getNextPlayerId(player_id):
        '''Get the opposite player for the given player_id'''
        # Makes 0 into 1, and 1 into 0
        return (player_id + 1) % 2

    def makeMove(self, player_id, x, y):
        '''Makes a move and returns if there was a hit'''
        # Check the validity of the move request
        if (self.game_status != "IN_PROGRESS"):
            raise PlayerError("Players can't make turns while the game isn't (yet) in progress")
        if (player_id not in (0, 1)):
            raise PlayerError("Player {} is not a valid player".format(player_id))
        if (self.turn_player != player_id):
            raise PlayerError("Player {} can't make a move when it's {}'s turn'".format(player_id, self.turn_player))

        # Get the opponent because we want to hit them, not us
        opponent_id = self.getNextPlayerId(player_id)
        hit_count = self.player_boards[opponent_id].checkHit(x, y)

        # If the opponent's health drops below 1 that means the game is over
        if (self.player_boards[opponent_id].getTotalHealth() < 1):
            self.game_status = "OVER"

        player_last_turns[player_id] = {'x':x, 'y':y}

        return hit_count

    def startIfEnoughPlayers(self):
        '''
        Starts the game if there is two boards.
        Pre-places ships in hardcoded locations for now.
        '''
        if (len(self.player_boards) != 2):
            return

        # Place ships in hardcoded places

        for board in self.player_boards:
            for ship in HARDCODED_SHIP_PLACEMENTS:
                self.player_boards[opponent_id].placeShip(
                    ship['x'], ship['y'], ship['allignment'], ship['length'])

        # Make game status ready for starting
        self.turn_player = 0
        self.game_status = "IN_PROGRESS"

    def joinPlayer(self):
        '''Tries to join a player into the game. Returns a board id.'''
        # Get the length from before. Which is the last index into the boards list
        before = len(self.player_boards)
        # Make sure there isn't too many players after this join
        if (before+1 > 2):
            raise PlayerError("Only max two players can join a game")
        # Append a board for the new player
        self.player_boards.append(BattleShipPlayerBoard())
        # Start if we have enough players
        self.startIfEnoughPlayers()
        # Return board index of the new player
        return before
