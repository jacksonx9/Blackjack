import numpy as np
import scipy.io as sio

from collections.abc import Iterable
from os import path

from data_game import DataGame
from enum_outcome import Outcome


class Generate():
    '''
    Creates and stores data in this format:
    y = | WIN/TIE/LOSS |
    X = | dealer_card | pre_hit_hand_value | player_aces | Hit/Stand | 2s | 3s |...
     4s | 5s | 6s | 7s | 8s | 9s | 10JQKs | As |
    '''
    data_row_num_elem = 13

    def __init__(self, rounds):
        self.data_file = 'blackjack_data.mat'
        self.result = []
        self.data = []

    def run(self):
        self.play_round(1)
        result_np = np.array(self.result).reshape(-1, 1)
        data_np = np.array(self.data).reshape(-1, Generate.data_row_num_elem)
        result_rows, _ = np.shape(result_np)
        data_rows, _ = np.shape(data_np)
        # print("result length {}: {}".format(len(self.result), self.result))
        # print("data length {}: {}".format(len(self.data)/13, self.data))
        # print("result_rows: {}, data_rows: {}".format(result_rows, data_rows))
        assert result_rows == data_rows
        sio.savemat(self.data_file, {'X': data_np, 'y': result_np})

    def play_round(self, player_hits):
        game = DataGame(6*52)
        game.deal_initial_cards()
        for _ in range(10):
            game.reset_initial_cards()
            game.deck.shuffle()
            (win, dealer_init_val, player_val_pre_last_hit,
                player_aces, cards_layout) = game.play(player_hits)

            if win == Outcome.INVALID:
                continue

            self._save_data(win, dealer_init_val, player_val_pre_last_hit,
                            player_aces, cards_layout)

    def _save_data(self, win, dealer_init_val, player_val_pre_last_hit,
                   player_val_final, cards_layout):
        self.result.append(win.value)
        self.data += self._flatten((dealer_init_val, player_val_pre_last_hit,
                                    player_val_final, cards_layout))

    def _flatten(self, items):
        result = []
        for item in items:
            if isinstance(item, tuple) or isinstance(item, Iterable):
                result += [elem for elem in item]
            else:
                result.append(item)

        return result

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


def main():
    g = Generate(1)
    g.run()


if __name__ == '__main__':
    main()
