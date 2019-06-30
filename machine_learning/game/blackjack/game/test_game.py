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

    def test_game_get_bet_default_min_bet(self):
        game = Game('', 100)
        with mock.patch('builtins.input', return_value=''):
            bet = game._get_bet(10, 2)
            self.assertEqual(bet, 10)

    def test_game_get_bet_double_min_bet(self):
        game = Game('', 100)
        with mock.patch('builtins.input', return_value=20):
            bet = game._get_bet(10, 2)
            self.assertEqual(bet, 20)

    def test_game_format_text(self):
        game = Game('', 100)
        resp = game.format_text('foo', 'testing')
        test = '{} > {}'.format('foo'.rjust(len('Dealer')), 'testing')
        self.assertEqual(resp, test)

    def test_game_sufficient_cards(self):
        game = Game('', 100)
        for _ in range(52*6 - (len(game.bot_players) + 2)*10 - 1):
            game.deck.next_card()
        self.assertTrue(game.sufficient_cards())

    def test_game_insufficient_cards(self):
        game = Game('', 100)
        for _ in range(52*6 - (len(game.bot_players) + 2)*10):
            game.deck.next_card()
        self.assertFalse(game.sufficient_cards())
