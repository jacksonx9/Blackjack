class Player():
    def __init__(self, name, chips):
        assert chips > 0
        self.chips = chips
        self.name = name
        self.hand = None

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

    def has_chips(self, amount=1):
        '''Does the player have sufficient chips to bet amount?'''
        assert amount >= 0
        return self.chips >= amount
