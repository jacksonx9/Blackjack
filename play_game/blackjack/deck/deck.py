import random, copy

from ..card.card import Card, RANK, SUIT


class Deck(): 
    '''Represents deck of 52 cards to be dealt to the player and dealer.'''

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in SUIT for rank in RANK]
    
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
        return self._cards.pop()

    def empty(self):
        '''Is the deck empty?'''
        return len(self._cards) is 0