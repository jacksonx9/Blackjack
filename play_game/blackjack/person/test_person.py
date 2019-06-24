from unittest import TestCase

from ..card.card import Card
from ..hand.hand import Hand
from .person import Person


class PersonTest(TestCase):
    '''Unit tests for the Blackjack person class'''

    def test_has_active_hands_true(self):
        person = Person("PlayerName")
        hand_1 = Hand(10)
        hand_2 = Hand(20)
        hand_2.active = False
        person.hands = [hand_1, hand_2]
        self.assertTrue(person.has_active_hands())
    
    def test_has_active_hands_false(self):
        person = Person("PlayerName")
        hand_1 = Hand(10)
        hand_2 = Hand(20)
        hand_1.active = False
        hand_2.active = False
        person.hands = [hand_1, hand_2]
        self.assertFalse(person.has_active_hands())

    def test_active_hands(self):
        person = Person("PlayerName")
        hand_1 = Hand(10)
        hand_2 = Hand(20)
        hand_3 = Hand(30)
        person.hands = [hand_1, hand_2, hand_3]
        result = person.active_hands()
        self.assertEqual(next(result), hand_1)
        self.assertEqual(next(result), hand_2)
        self.assertEqual(next(result), hand_3)
    
    def test_active_hands_status_change(self):
        '''Available hands should adjust by status'''
        person = Person("PlayerName")
        hand_1 = Hand(10)
        hand_2 = Hand(20)
        hand_3 = Hand(30)
        person.hands = [hand_1, hand_2, hand_3]
        result = person.active_hands()
        self.assertEqual(next(result), hand_1)
        hand_2.active = False
        self.assertEqual(next(result), hand_3)