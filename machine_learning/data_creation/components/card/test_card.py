from unittest import TestCase

from .card import Card


class CardTest(TestCase):
    def test_card_init_valid_card(self):
        '''No error raised.'''
        card = Card("6")

    def test_card_init_invalid_card(self):
        with self.assertRaises(AssertionError):
            _ = Card("11")

    def test_card_stringify_one_digit(self):
        card = Card("A")
        self.assertEqual(str(card), " A")

    def test_card_stringify_two_digit(self):
        card = Card("10")
        self.assertEqual(str(card), "10")

    def test_card_value_numeric(self):
        card = Card("2")
        self.assertEqual(card.value(), 2)

    def test_card_value_face_card(self):
        card = Card("Q")
        self.assertEqual(card.value(), 10)

    def test_card_value_ace(self):
        card = Card("A")
        self.assertEqual(card.value(), 11)

    def test_card_ace_true(self):
        card = Card("A")
        self.assertTrue(card.ace())

    def test_card_ace_false(self):
        card = Card("9")
        self.assertFalse(card.ace())

    def test_card_face_card_true(self):
        card = Card("K")
        self.assertTrue(card._face_card())

    def test_card_face_card_false(self):
        card = Card("9")
        self.assertFalse(card._face_card())
