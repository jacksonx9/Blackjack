from unittest import TestCase, mock

from ..hand.hand import Hand
from .game import Game


class GameTest(TestCase):
    '''Unit tests for the Blackjack Game class.'''

    def test_init_creates_players(self):
        names = 'player1, player2, player3'.split()
        chips = 100
        game = Game(names, chips)
        self.assertEqual(len(game.players), 3)
        self.assertEqual(game.players[0].name, names[0])
        self.assertEqual(game.players[1].name, names[1])
        self.assertEqual(game.players[2].name, names[2])

    def test_init_max_name_len_calculated_dealer(self):
        names = 'p1 p2 p3'.split()
        game = Game(names, 100)
        self.assertEqual(game.max_name_len, len('Dealer'))
    
    def test_init_max_name_len_calculated_player_name(self):
        names = 'p1 p2 p3 longname'.split()
        game = Game(names, 100)
        self.assertEqual(game.max_name_len, len('longname'))

    def test_deal_card(self):
        names = 'p1 p2 p3 longname'.split()
        game = Game(names, 100)
        hand = Hand(0)
        game._deal_card(game.players[0].name, hand)
        self.assertTrue(len(hand), 1)

    def test_get_bet_min_bet(self):
        names = 'p1 p2 p3 longname'.split()
        game = Game(names, 100)
        with mock.patch('builtins.input', return_value=10):
            bet = game._get_bet(game.players[0], 'question', 10, 2)
            self.assertEqual(bet, 10)

    def test_get_bet_double_min_bet(self):
        names = 'p1 p2 p3 longname'.split()
        game = Game(names, 100)
        with mock.patch('builtins.input', return_value=20):
            bet = game._get_bet(game.players[0], 'question', 10, 2)
            self.assertEqual(bet, 20)

    def test_format_text(self):
        '''Format text produces desired output.'''
        game = Game(['foo'], 100)
        blue = '\x1b[34m'
        stop = '\x1b[0m'
        resp = game.format_text('foo', 'testing', 'blue')
        test = '{}{} > {}{}'.format(blue, 'foo'.rjust(len('Dealer')), 'testing', stop)
        self.assertEqual(resp, test)

    def test_players_with_chips(self):
        game = Game(['foo'], 100)
        self.assertTrue(game.players_with_chips())
    
    def test_players_without_chips(self):
        game = Game(['foo'], 10)
        game.players[0].chips = 0
        self.assertFalse(game.players_with_chips())

    def test_active_players(self):
        game = Game(['p1', 'p2', 'p3'], 100)
        for player in game.players:
            player.hands.append(Hand(10))
        result = game.active_players()
        self.assertEqual(next(result).name, 'p1')
        self.assertEqual(next(result).name, 'p2')
        self.assertEqual(next(result).name, 'p3')
    
    def test_active_players_status_change(self):
        game = Game(['p1', 'p2', 'p3'], 100)
        for player in game.players:
            player.hands.append(Hand(10))
        result = game.active_players()
        self.assertEqual(next(result).name, 'p1')
        game.players[1].hands[0].active = False
        self.assertEqual(next(result).name, 'p3')

    def test_has_active_hands(self):
        game = Game(['foo'], 100)
        game.players[0].hands.append(Hand(10))
        self.assertTrue(game.has_active_hands())
    
    def test_has_active_hands_none_active(self):
        game = Game(['foo'], 100)
        game.players[0].hands.append(Hand(10))
        game.players[0].hands[0].active = False
        self.assertFalse(game.has_active_hands())