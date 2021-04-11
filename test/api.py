import json
from pocha import before, beforeEach, describe, it
from hamcrest import *

import main
from db import wipeDatabase, DbBattleShipGame

from main import app as server_app

def assertResponseJson(res, status_code, data, description=''):
    assert_that(res.status_code, equal_to(status_code), description)
    assert_that(json.loads(res.get_data()), equal_to(data), description)

def responseJsonToPy(res):
    return json.loads(res.get_data())

@describe('API Tests')
def apiTests():
    server_app.config['TESTING'] = True
    app = server_app.test_client()

    @beforeEach
    def _beforeEach():
        wipeDatabase()

    @it("Can list all games")
    def canListAllGames():
        # No games
        res = app.get('/games')
        assertResponseJson(res, 200, [], 'Hands empty list when no games')

        DbBattleShipGame.create().save()
        DbBattleShipGame.create().save()
        DbBattleShipGame.create().save()

        res = app.get('/games')
        assert_that(res.status_code, equal_to(200), 'Lists 3 games')
        assert_that(len(json.loads(res.get_data())), equal_to(3), 'Lists 3 games')

    @it("Id on global list matches id for getting the game")
    def displayedIdMatchesEndpoint():
        # Seed with one game
        DbBattleShipGame.create().save()

        res = app.get('/games')
        assert_that(res.status_code, equal_to(200))
        games_list = responseJsonToPy(res)

        res = app.get('/games/{}'.format(games_list[0]['id']))
        assert_that(res.status_code, equal_to(200))
        game_0 = responseJsonToPy(res)
        assert_that(games_list[0], equal_to(game_0))

    @it("Can create a game")
    def canCreateGame():
        res = app.get('/games')
        assertResponseJson(res, 200, [], 'Games is empty')

        res = app.post('/games')
        assert_that(res.status_code, equal_to(201), 'Has proper game creation response')

        creation_data = responseJsonToPy(res)
        assert_that(creation_data['joined_game_id'], instance_of(int), 'joined_game_id is an int')
        assert_that(creation_data['player_id'], instance_of(int), 'player_id is an int')

        res = app.get('/games/{}'.format(creation_data['joined_game_id']))
        assert_that(res.status_code, equal_to(200), 'Can retrieve created game')

        # Check if the game initialized properly

        get_data = responseJsonToPy(res)
        assert_that(get_data['id'], equal_to(creation_data['joined_game_id']))
        assert_that(get_data['status'], equal_to("PRE_GAME"), "Game hasn't started yet because we're the only player")
        assert_that(get_data['player_count'], equal_to(1), "There's only one player")
        assert_that(get_data['turn_player'], none(), "No turn selected yet because we're pregame")

    @it("Can join created game")
    def canJoinGame():
        # Create game
        res = app.post('/games')
        assert_that(res.status_code, equal_to(201), res.get_data())
        creation_data = responseJsonToPy(res)

        res = app.get('/games/{}'.format(creation_data['joined_game_id']))
        assert_that(res.status_code, equal_to(200), 'Can retrieve created game')
        old_game = responseJsonToPy(res)

        # Join game
        res = app.post('/games/{}'.format(creation_data['joined_game_id']))
        assert_that(res.status_code, equal_to(200), res.get_data())
        join_data = responseJsonToPy(res)

        res = app.get('/games/{}'.format(creation_data['joined_game_id']))
        assert_that(res.status_code, equal_to(200), 'Can retrieve created game')
        new_game = responseJsonToPy(res)

        assert_that(old_game, is_not(equal_to(new_game)), 'The game should have changed by us joining it')
        assert_that(new_game['id'], equal_to(old_game['id']), "id shouldn't update by us joining the game")
        # Testing the same things here as canCreateGame
        assert_that(new_game['status'], equal_to("IN_PROGRESS"), "Game has started because we joined two players")
        assert_that(new_game['player_count'], equal_to(2), "There's two players after we joined")
        assert_that(new_game['turn_player'], equal_to(0), "No turn selected yet because we're pregame")
