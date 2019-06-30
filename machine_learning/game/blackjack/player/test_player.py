from unittest import TestCase

from .. import Card
from .. import Hand
from .player import Player


class PlayerTest(TestCase):
    '''Unit tests for the Blackjack player class'''

    def test_player_active_hand(self):
        player = Player('PlayerName', 100)
        hand = Hand(0)
        player.hands = [hand]
        self.assertEqual(hand, next(player.active_hands()))

    def test_player_active_hand_change_status(self):
        player = Player('PlayerName', 100)
        hand1 = Hand(0)
        hand2 = Hand(2)
        player.hands = [hand1, hand2]
        result = player.active_hands()
        player.hands[0].active = False
        self.assertEqual(hand2, next(result))

    def test_player_active_hand_none_active(self):
        player = Player('PlayerName', 100)
        player.hands = [Hand(0)]
        player.hands[0].active = False
        with self.assertRaises(StopIteration):
            next(player.active_hands())

    def test_game_has_active_hands_active_player(self):
        player = Player('PlayerName', 100)
        player.hands = [Hand(0)]
        self.assertTrue(player.has_active_hands())

    def test_game_player_has_active_hands_none_active(self):
        player = Player('PlayerName', 100)
        player.hands = [Hand(0)]
        player.hands[0].active = False
        self.assertFalse(player.has_active_hands())

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

    def test_player_split_hand_possible(self):
        player = Player('PlayerName', 100)
        hand = Hand(50)
        hand.add_card(Card('Q'))
        hand.add_card(Card('Q'))
        self.assertTrue(player.can_split(hand))

    def test_player_split_hand_3_cards(self):
        player = Player('PlayerName', 100)
        hand = Hand(50)
        hand.add_card(Card('J'))
        hand.add_card(Card('J'))
        hand.add_card(Card('J'))
        self.assertFalse(player.can_split(hand))

    def test_player_split_hand_insufficient_chips(self):
        player = Player('PlayerName', 100)
        hand = Hand(101)
        hand.add_card(Card('J'))
        hand.add_card(Card('J'))
        self.assertFalse(player.can_split(hand))

    def test_player_has_chips_for_player_whole_stack(self):
        player = Player('PlayerName', 100)
        self.assertTrue(player.has_chips(99))

    def test_player_has_chips_for_more_than_player_whole_stack(self):
        player = Player('PlayerName', 100)
        self.assertFalse(player.has_chips(101))
