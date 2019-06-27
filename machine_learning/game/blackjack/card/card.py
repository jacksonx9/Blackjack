RANK = [str(n) for n in range(2, 11)] + list('JQKA')


class Card(object):
    '''Represents a playing card'''

    def __init__(self, rank):
        assert rank in RANK
        self.rank = rank

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({:>2})'.format(class_name, self.rank)

    def __str__(self):
        return '{:>2}'.format(self.rank)

    def value(self):
        '''Computes the value of the card.'''
        if self.ace():
            value = 11
        elif self._face_card():
            value = 10
        else:
            value = int(self.rank)
        return value

    def ace(self):
        '''Is this card an ace?'''
        return self.rank == 'A'

    def _face_card(self):
        '''Is this card a face card?'''
        return self.rank == 'J' or self.rank == 'Q' or self.rank == 'K'
