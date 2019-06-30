from unittest import TestCase

from .bot_player import BotPlayer
from ..hand.hand import Hand


class BotPlayerTest(TestCase):
    def test_init_name(self):
        name = "username"
        player = BotPlayer(name)
        self.assertEqual(name, player.name)

    def test_init_hand(self):
        name = "username"
        player = BotPlayer(name)
        hand = Hand(0)
        player.hand = hand
        self.assertEqual(hand, player.hand)
