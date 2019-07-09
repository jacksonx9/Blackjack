import numpy as np
import scipy.io as sio

from collections import Iterable
from os import path

from .data_game import DataGame
from .enum_outcome import Outcome


class Generate():
    '''
    Creates and stores data in this format:
    | hand_value | num_aces | dealer_card | H/s | win/loss | 2s | 3s |...
     4s | 5s | 6s | 7s | 8s | 9s | 10JQKs | As |
    '''

    def __init__(self):
        self.data_file = 'blackjack_data.mat'

    def run(self):
        pass

    def play_round(self, player_hits):
        for _ in range(10):
            game = DataGame(6*52)
            (win, dealer_init_val, player_val_pre_last_hit,
                player_val_final, cards_layout) = game.play(player_hits)
            
            if win == Outcome.INVALID:
                continue

    def _reset_cards(self):
        pass

    def _create_mat_file(self):
        if not path.exists("blackjack_data.mat"):
            vect = np.arange(10)
            vect.reshape(10,)
            sio.savemat('blackjack_data.mat', {'vect': vect})

    def _add_data_to_mat_file(self, data):
        # sort data
        # hand value, has ace
        # https://github.com/scipy/scipy/issues/2967
        pass

    def _player_hand_value(self):
        hand = self.game.player.hand

    def _player_number_of_aces(self):
        hand = self.game.player.hand

    def _remaining_cards(self):
        deck = self.game.deck
        # number of cards for each value

    def flatten(items):
        for x in items:
            if isinstance(x, tuple) or isinstance(x, Iterable):
                yield from flatten(x)
            else:
                yield x

    def _loading_bar(self):
        pass
        # https://docs.scipy.org/doc/scipy/reference/tutorial/io.html

    def printProgressBar(iteration, total, prefix='', suffix='', decimals=1,
                         length=100, fill='█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent
                                      complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration /
                                                                float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
        # Print New Line on Complete
        if iteration == total:
            print()

        '''
        from time import sleep

# A List of Items
items = list(range(0, 57))
l = len(items)

# Initial call to print 0% progress
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i, item in enumerate(items):
    # Do stuff...
    sleep(0.1)
    # Update Progress Bar
    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete',
                    length = 50)
    '''
