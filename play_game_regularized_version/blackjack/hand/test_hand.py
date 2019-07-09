from unittest import TestCase

from .hand import Hand
from ..card.card import Card


class HandTestCase(TestCase):
    def test_hand_representation(self):
        hand = Hand()
        hand.add_card(Card('K', '♧'))
        hand.add_card(Card('7', '♡'))
        self.assertEqual(repr(hand), 'Hand( K♧, 7♡)')

    def test_hand_stringify(self):
        hand = Hand()
        hand.add_card(Card('10', '♤'))
        hand.add_card(Card('A', '♢'))
        self.assertEqual(str(hand), '10♤, A♢')

    def test_hand_add_card(self):
        hand = Hand()
        card = Card('9', '♤')
        hand.add_card(card)
        self.assertEqual(len(hand), 1)

    def test_hand_value_soft_less_than_21(self):
        hand = Hand()
        hand.add_card(Card('A', '♤'))
        hand.add_card(Card('9', '♢'))
        self.assertEqual(hand.value(), 20)

    def test_hand_value_soft_over_21(self):
        hand = Hand()
        hand.add_card(Card('A', '♤'))
        hand.add_card(Card('A', '♢'))
        self.assertEqual(hand.value(), 12)

    def test_hand_value_hard_over_21(self):
        hand = Hand()
        hand.add_card(Card('A', '♤'))
        hand.add_card(Card('A', '♤'))
        hand.add_card(Card('K', '♤'))
        hand.add_card(Card('Q', '♤'))
        self.assertEqual(hand.value(), 22)

    def test_hand_blackjack_true(self):
        hand = Hand()
        hand.add_card(Card('Q', '♢'))
        hand.add_card(Card('A', '♤'))
        self.assertTrue(hand.blackjack())

    def test_hand_blackjack_too_many_cards(self):
        hand = Hand()
        hand.add_card(Card('Q', '♢'))
        hand.add_card(Card('5', '♡'))
        hand.add_card(Card('6', '♡'))
        self.assertFalse(hand.blackjack())

    def test_hand_blackjack_not_21(self):
        hand = Hand()
        hand.add_card(Card('Q', '♢'))
        hand.add_card(Card('6', '♡'))
        hand.add_card(Card('6', '♡'))
        self.assertFalse(hand.blackjack())

    def test_hand_twenty_one_true(self):
        hand = Hand()
        hand.add_card(Card('K', '♢'))
        hand.add_card(Card('7', '♤'))
        hand.add_card(Card('4', '♧'))
        self.assertTrue(hand.twenty_one())

    def test_hand_twenty_one_false(self):
        hand = Hand()
        hand.add_card(Card('J', '♤'))
        hand.add_card(Card('8', '♧'))
        self.assertFalse(hand.twenty_one())

    def test_hand_bust_true(self):
        hand = Hand()
        hand.add_card(Card('K', '♢'))
        hand.add_card(Card('7', '♤'))
        hand.add_card(Card('5', '♡'))
        self.assertTrue(hand.bust())

    def test_hand_bust_false(self):
        hand = Hand()
        hand.add_card(Card('K', '♢'))
        hand.add_card(Card('7', '♤'))
        self.assertFalse(hand.bust())

    def test_hand_split_pair(self):
        card = Card('J', '♡')
        hand = Hand()
        hand.add_card(card)
        hand.add_card(card)
        new_hand = hand.split()
        self.assertIsInstance(new_hand, Hand)
        self.assertTrue(str(hand) == str(new_hand))

    def test_hand_split_non_pair(self):
        hand = Hand()
        hand.add_card(Card('2', '♧'))
        hand.add_card(Card('3', '♧'))
        with self.assertRaises(AssertionError):
            hand.split()
