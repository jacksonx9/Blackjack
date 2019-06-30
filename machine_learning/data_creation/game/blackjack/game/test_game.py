from unittest import TestCase, mock
from mock import patch

from ..card.card import Card
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

    def test_game_setup(self):
        game = Game('', 100)
        org_num_cards = len(game.deck)
        with mock.patch('builtins.input', return_value=20):
            game.setup()
        self.assertEqual(2, len(game.player.hand))
        self.assertEqual(2, len(game.dealer))
        for bot in game.bot_players:
            self.assertEqual(2, len(bot.hand))
        num_bots = len(game.bot_players)
        post_num_cards = len(game.deck)
        self.assertEqual(org_num_cards - 4 - 2*num_bots, post_num_cards)

    def test_game_check_for_blackjack_player_and_dealer_blackjack(self):
        game = Game('Player', 100)
        game.dealer = Hand()
        game.player.hand = Hand(10)
        game.dealer.add_card(Card('A'))
        game.dealer.add_card(Card('10'))
        game.player.hand.add_card(Card('A'))
        game.player.hand.add_card(Card('10'))
        with patch.object(game.player, 'push') as mock:
            game.check_for_blackjack()
        self.assertFalse(game.playing)
        mock.assert_called_once_with(10)
    
    def test_game_check_for_blackjack_player_blackjack(self):
        game = Game('Player', 100)
        game.dealer = Hand()
        game.player.hand = Hand(10)
        game.dealer.add_card(Card('10'))
        game.dealer.add_card(Card('10'))
        game.player.hand.add_card(Card('A'))
        game.player.hand.add_card(Card('10'))
        with patch.object(game, 'settle_outcome') as mock:
            game.check_for_blackjack()
        self.assertFalse(game.playing)
        mock.assert_called_once_with()

    def test_game_check_for_blackjack_dealer_blackjack(self):
        game = Game('Player', 100)
        game.dealer = Hand()
        game.player.hand = Hand(10)
        game.dealer.add_card(Card('A'))
        game.dealer.add_card(Card('10'))
        game.player.hand.add_card(Card('10'))
        game.player.hand.add_card(Card('10'))
        self.assertFalse(game.playing)

    def test_game_settle_outcome(self):
        pass

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
