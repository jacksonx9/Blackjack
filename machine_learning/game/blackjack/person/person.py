class Person():
    '''Represents a player or the dealer in the game'''

    def __init__(self, name):        
        self.name = name
        self.hands = []
        self.results = {'wins': 0, 'ties': 0, 'losses': 0}

    def active_hands(self):
        '''Generator of hands still active in this round.'''
        for hand in self.hands:
            if hand.active:
                yield hand

    def has_active_hands(self):
        '''Does the player have any active hands?'''
        return list(h for h in self.hands if h.active)