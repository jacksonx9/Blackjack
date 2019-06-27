from .. import Person


class Dealer(Person):
    def __init__(self, name):
        Person.__init__(self, name)

    def first(self):
        '''Returns the first card in the hand'''
        assert self.cards
        return self.cards[0]

    def last(self):
        '''Returns the last card in the hand'''
        assert self.cards
        return self.cards[-1]
