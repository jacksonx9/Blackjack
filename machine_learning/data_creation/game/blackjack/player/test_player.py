from unittest import TestCase

from .. import Card
from .. import Hand
from .player import Player


class PlayerTest(TestCase):
    '''Unit tests for the Blackjack player class'''

    def test_player_wins_bet(self):
        player = Player('PlayerName', 100)
        player.win(10)
        self.assertEqual(player.chips, 120)

    def test_player_pushes_bet(self):
        player = Player('PlayerName', 100)
        player.push(10)
        self.assertEqual(player.chips, 110)

    def test_player_can_bet(self):
        player = Player('PlayerName', 100)
        bet = player.bet(10)
        self.assertEqual(bet, 10)
        self.assertEqual(player.chips, 90)

    def test_player_has_chips_for_player_whole_stack(self):
        player = Player('PlayerName', 100)
        self.assertTrue(player.has_chips(99))

    def test_player_has_chips_for_more_than_player_whole_stack(self):
        player = Player('PlayerName', 100)
        self.assertFalse(player.has_chips(101))
