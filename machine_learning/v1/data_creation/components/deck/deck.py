import random

from ..card.card import Card, RANK


class Deck():
    '''Represents deck of 52 cards to be dealt to the player and dealer.'''

    def __init__(self, num_decks=1):
        self._cards = [Card(rank) for rank in RANK] * 4 * num_decks

    def __len__(self):
        return len(self._cards)

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({})'.format(class_name, self._cards)

    def __str__(self):
        return str(self._cards)

    def shuffle(self):
        '''Randomly shuffle the deck of cards'''
        random.shuffle(self._cards)

    def next_card(self):
        '''Deal next card in deck.'''
        return self._cards.pop(0)

    def card_at(self, index):
        '''Value of card at index.'''
        return self._cards[index]

    def set_total_cards(self, length):
        '''Deals cards until deck has len cards.'''
        assert length > 20
        assert len(self._cards) >= length

        while len(self._cards) != length:
            self.next_card()

    def card_divide(self):
        card_rank_count = [0] * 10
        for card in self._cards:
            card_idx = card.value() - 2  # start a 0th idx and no card = 1
            card_rank_count[card_idx] += 1

        return card_rank_count
