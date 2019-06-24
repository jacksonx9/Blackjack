from .. import Person

class Player(Person):
    def __init__(self, name, chips, color='green'):
        assert chips > 0
        self.chips = chips
        self.insurance = 0
        Person.__init__(self, name, color)

    def win(self, bet, odds=1):
        '''Player wins at the odds provided'''
        assert bet > 0
        assert odds >= 1
        self.chips += int(bet * (odds + 1))
        self.results['wins'] += 1 #TODO: Remove wins

    def loss(self):
        '''Player loses their bet'''
        self.results['losses'] += 1 #TODO: Remove losses

    def push(self, bet): #TODO: When is a bet preserved????????/
        '''Player bet is preserved'''
        assert bet > 0
        self.chips += bet
        self.results['ties'] += 1 #TODO: Remove ties

    def bet(self, bet):
        '''Player places a bet'''
        assert bet > 0
        assert self.has_chips(bet)
        self.chips -= bet
        return bet
    
    def can_double_down(self, hand):
        '''
        Does player has at least the amount of chips in pot and has 
        either two cards or hand value of 9, 10, or 11?
        '''
        return (self.has_chips(hand.stake) and (len(hand.cards) == 2 or
            hand.value() in (9, 10, 11)))

    def can_split(self, hand):
        '''Does the player have enough money to split and a pair?'''
        return self.has_chips(hand.stake) and hand.pair()

    def has_chips(self, amount=1):
        '''Does the player have sufficient chips to bet amount?'''
        assert amount >= 0
        return self.chips >= amount