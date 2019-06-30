from unittest import TestCase, mock

from ..hand.hand import Hand
from .game import Game


class GameTest(TestCase):
    '''Unit tests for the Blackjack Game class.'''

    def test_game_init_max_name_len_calculated_dealer(self):
        name = 'p1'
        game = Game(name, 100)
        self.assertEqual(game.max_name_len, len('Dealer'))

    def test_game_init_max_name_len_calculated_player_name(self):
        name = 'longname'
        game = Game(name, 100)
        self.assertEqual(game.max_name_len, len('longname'))

    def test_game_deal_card(self):
        game = Game('', 100)
        hand = Hand(0)
        game._deal_card(game.player.name, hand)
        self.assertTrue(len(hand), 1)

    def test_game_get_bet_min_bet(self):
        game = Game('', 100)
        with mock.patch('builtins.input', return_value=10):
            bet = game._get_bet(10, 2)
            self.assertEqual(bet, 10)

    def test_game_get_bet_double_min_bet(self):
        game = Game('', 100)
        with mock.patch('builtins.input', return_value=20):
            bet = game._get_bet(10, 2)
            self.assertEqual(bet, 20)

    def test_game_format_text(self):
        '''Format text produces desired output.'''
        game = Game('', 100)
        stop = '\x1b[0m'
        resp = game.format_text('foo', 'testing')
        test = '{} > {}'.format('foo'.rjust(len('Dealer')), 'testing')
        self.assertEqual(resp, test)

    def test_game_player_with_chips(self):
        game = Game('', 100)
        self.assertTrue(game.player.has_chips())

    def test_game_player_without_chips(self):
        game = Game('', 10)
        game.player.chips = 0
        self.assertFalse(game.player.has_chips())

    def test_game_has_active_hands_active_player(self):
        game = Game('', 100)
        game.player.hands.append(Hand(10))
        self.assertTrue(game.player.has_active_hands())

    def test_game_player_has_active_hands_none_active(self):
        game = Game('', 100)
        game.player.hands.append(Hand(10))
        game.player.hands[0].active = False
        self.assertFalse(game.player.has_active_hands())
