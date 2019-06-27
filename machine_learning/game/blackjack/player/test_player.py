from unittest import TestCase

from .. import Card
from .. import Hand
from .player import Player


class PlayerTest(TestCase):
    '''Unit tests for the Blackjack player class'''

    def test_wins_bet(self):
        player = Player('PlayerName', 100)
        player.win(10, 1.5)
        self.assertEqual(player.chips, 125)
        self.assertEqual(player.results['wins'], 1) # wins still here?

    def test_loses_bet(self):
        player = Player('PlayerName', 100)
        player.loss()
        self.assertEqual(player.chips, 100)
        self.assertEqual(player.results['losses'], 1) # wins still here?

    def test_pushes_bet(self):
        player = Player('PlayerName', 100)
        player.push(10)
        self.assertEqual(player.chips, 110)
        self.assertEqual(player.results['ties'], 1) # wins still here?

    def test_can_bet(self):
        player = Player('PlayerName', 100)
        bet = player.bet(10)
        self.assertEqual(bet, 10)
        self.assertEqual(player.chips, 90)

    def test_double_down_hand_value_9_10_11(self):
        player = Player('PlayerName', 100)
        hand = Hand(50)
        hand.add_card(Card('9', '♧'))
        self.assertTrue(player.can_double_down(hand))
        hand.cards.pop()
        hand.add_card(Card('10', '♧'))
        self.assertTrue(player.can_double_down(hand))
        hand.cards.pop()
        hand.add_card(Card('A', '♤'))
        self.assertTrue(player.can_double_down(hand))

    def test_double_down_hand_value_8_12(self):
        player = Player('PlayerName', 100)
        hand = Hand(51)
        hand.add_card(Card('4', '♧'))
        hand.add_card(Card('2', '♧'))
        hand.add_card(Card('2', '♧'))
        self.assertFalse(player.can_double_down(hand))
        hand.add_card(Card('4', '♤'))
        self.assertFalse(player.can_double_down(hand))

    def test_double_down_sufficient_chips_2_cards(self):
        player = Player('PlayerName', 100)
        hand = Hand(50)
        hand.add_card(Card('6', '♢'))
        hand.add_card(Card('8', '♤'))
        self.assertTrue(player.can_double_down(hand))
    
    def test_double_down_sufficient_chips_3_cards(self):
        player = Player('PlayerName', 100)
        hand = Hand(50)
        hand.add_card(Card('2', '♢'))
        hand.add_card(Card('8', '♧'))
        hand.add_card(Card('9', '♤'))
        self.assertFalse(player.can_double_down(hand))

    def test_double_down_insufficent_chips(self):
        player = Player('PlayerName', 100)
        hand = Hand(51)
        hand.add_card(Card('7', '♡'))
        hand.add_card(Card('5', '♡'))
        hand.add_card(Card('3', '♤'))
        self.assertFalse(player.can_double_down(hand)) 

    def test_split_hand_possible(self):
        player = Player('PlayerName', 100)
        hand = Hand(50)
        hand.add_card(Card('Q', '♡'))
        hand.add_card(Card('Q', '♡'))
        self.assertTrue(player.can_split(hand))
    
    def test_split_hand_3_cards(self):
        player = Player('PlayerName', 100)
        hand = Hand(50)
        hand.add_card(Card('J', '♡'))
        hand.add_card(Card('J', '♡'))
        hand.add_card(Card('J', '♡'))
        self.assertFalse(player.can_split(hand))
    
    def test_split_hand_insufficient_chips(self):
        player = Player('PlayerName', 100)
        hand = Hand(101)
        hand.add_card(Card('J', '♡'))
        hand.add_card(Card('J', '♡'))
        self.assertFalse(player.can_split(hand))
    
    def test_has_chips_for_player_whole_stack(self):
        player = Player('PlayerName', 100)
        self.assertTrue(player.has_chips(99))

    def test_has_chips_for_more_than_player_whole_stack(self):
        player = Player('PlayerName', 100)
        self.assertFalse(player.has_chips(101))