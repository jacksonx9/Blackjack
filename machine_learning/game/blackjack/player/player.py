class Player():
    def __init__(self, name, chips):
        assert chips > 0
        self.chips = chips
        self.name = name
        self.hands = []

    def active_hands(self):
        '''Generator of hands still active in this round.'''
        for hand in self.hands:
            if hand.active:
                yield hand

    def has_active_hands(self):
        '''Does the player have any active hands?'''
        return list(h for h in self.hands if h.active)

    def win(self, bet):
        '''Player wins at the odds provided'''
        assert bet > 0
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
