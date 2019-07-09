from unittest import TestCase

from .deck import Deck


class DeckTest(TestCase):
    def test_deck_init_len(self):
        deck = Deck()
        self.assertEqual(len(deck), 52)

    def test_deck_repr(self):
        deck = Deck()
        self.assertEqual('Deck(' + str(deck._cards) + ')', repr(deck))

    def test_deck_str(self):
        deck = Deck()
        self.assertEqual(str(deck._cards), str(deck))

    def test_deck_next_card(self):
        deck = Deck()
        _ = deck.next_card()
        self.assertEqual(len(deck), 51)

    def test_deck_shuffle(self):
        deck1 = Deck()
        deck1.shuffle()
        deck2 = Deck()
        deck2.shuffle()
        self.assertNotEqual(str(deck1), str(deck2))

    def test_deck_card_divide(self):
        deck = Deck()

        first_card = deck.card_at(0)
        print(first_card)
        self.assertEqual(52, len(deck))
        self.assertEqual(deck.next_card(), first_card)

    def test_deck_set_total_cards(self):
        deck = Deck()
        deck.set_total_cards(21)
        self.assertEqual(21, len(deck))

    def test_deck_card_divide_init(self):
        deck = Deck()
        expected = [4]*8 + [16] + [4]
        self.assertEqual(expected, deck.card_divide())

    def test_deck_card_divide_after_removal(self):
        deck = Deck()
        deck.next_card()
        expected = [3] + [4]*7 + [16] + [4]
        self.assertEqual(expected, deck.card_divide())
