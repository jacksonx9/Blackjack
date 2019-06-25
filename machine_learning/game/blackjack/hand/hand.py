class Hand():
    def __init__(self, stake=0):
        self.cards = []
        self.stake = stake
        self.active = True

    def __repr__(self):
        class_name = type(self).__name__
        return '{}('.format(class_name) + ','.join(str(card) for card in self.cards) + ')'

    def __str__(self):
        return ','.join(str(card) for card in self.cards)
    
    def __len__(self):
        return len(self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        '''Calculate the value of the hand. Aces can be 11 or 1.'''
        aces = sum(1 for c in self.cards if c.ace())
        value = sum(c.value() for c in self.cards)
        while value > 21 and aces > 0:
            aces -= 1
            value -= 10
        return value

    def blackjack(self):
        '''Determine if there are only 2 cards add to 21.'''
        return len(self.cards) == 2 and self.value() == 21

    def twenty_one(self):
        return self.value() == 21

    def bust(self):
        '''Determine if the hand is worth more than 21.'''
        return self.value() > 21

    def pair(self):
        '''Determine if the hand is two cards the same.'''
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[-1].rank

    def split(self):
        '''Split this hand into two hands if it can be split.'''
        assert self.pair()
        card = self.cards.pop()
        hand = Hand(self.stake)
        hand.add_card(card)
        return hand