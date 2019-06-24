from unittest import TestCase

from .deck import Deck


class DeckTest(TestCase):
    def test_init_len(self):
        deck = Deck()
        self.assertEqual(len(deck), 52)

    def test_repr(self):
        deck = Deck()
        self.assertEqual('Deck(' + str(deck._cards) + ')', repr(deck))

    def test_next_card(self):
        deck = Deck()
        _ = deck.next_card()
        self.assertEqual(len(deck), 51)

    def test_shuffle(self):
        deck1 = Deck()
        deck1.shuffle()
        deck2 = Deck()
        deck2.shuffle()
        self.assertNotEqual(str(deck1), str(deck2))

    def test_is_empty(self):
        deck = Deck()

        for _ in range(52):
            _ = deck.next_card()

        self.assertTrue(deck.empty())