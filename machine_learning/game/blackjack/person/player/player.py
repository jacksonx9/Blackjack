from .. import Person


class Player(Person):
    def __init__(self, name, chips):
        assert chips > 0
        self.chips = chips
        Person.__init__(self, name)

    def win(self, bet):
        '''Player wins at the odds provided'''
        assert bet > 0
        assert odds >= 1
        self.chips += int(bet) * 2

    def push(self, bet):
        '''When there is a draw.'''
        assert bet > 0
        self.chips += bet

    def bet(self, bet):
        '''Player places a bet'''
        assert bet > 0
        assert self.has_chips(bet)
        self.chips -= bet
        return bet

    def can_split(self, hand):
        '''Does the player have enough money to split and a pair?'''
        return self.has_chips(hand.stake) and hand.pair()

    def has_chips(self, amount=1):
        '''Does the player have sufficient chips to bet amount?'''
        assert amount >= 0
        return self.chips >= amount
