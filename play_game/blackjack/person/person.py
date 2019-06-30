from termcolor import COLORS


SYSTEM_COLORS = ['grey', 'white']
PLAYER_COLORS = list(c for c in COLORS.keys() if c not in SYSTEM_COLORS)


class Person():
    '''Represents a player or the dealer in the game'''

    def __init__(self, name, color='green'):
        assert color in PLAYER_COLORS
        self.name = name
        self.color = color
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
