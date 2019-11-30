import random
import numpy as np
import scipy.io as sio

from collections.abc import Iterable


class Game:
    '''Runs simulation of blackjack games'''
    '''
    Creates and stores data in this format:
    y = | Hit/Stand |
    X = | dealer_card | pre_hit_hand_value |
        2s | 3s | 4s | 5s | 6s | 7s | 8s | 9s | 10JQKs | As |
    '''

    min_cards = 20
    suits = 4
    # Note: J, Q, and K is treated as 10
    poss_cards = [n for n in range(2, 12)]
    X_num_elem = 12
    num_simulations = 1000

    def __init__(self, num_decks=6):
        self.data_file = './logistic_regression/blackjack_data.mat'
        self.decks = num_decks
        self.result = []
        self.data = []

    def run(self):
        self.simulate()
        result_np = np.array(self.result, dtype=np.double).reshape(-1, 1)
        data_np = np.array(
            self.data, dtype=np.double).reshape(-1, Game.X_num_elem)
        result_rows, _ = np.shape(result_np)
        data_rows, _ = np.shape(data_np)
        # print("result length {}: {}".format(len(self.result), self.result))
        # print("data length {}: {}".format(len(self.data)/13, self.data))
        # print("result_rows: {}, data_rows: {}".format(result_rows,
        #                                               data_rows))
        assert result_rows == data_rows
        sio.savemat(self.data_file, {'X': data_np, 'y': result_np})


    def simulate(self):
        for _ in range(Game.num_simulations):
            for dc_idx, dc_val in enumerate(Game.poss_cards):
                for pc1_idx, pc1_val in enumerate(Game.poss_cards):
                    for pc2_idx, pc2_val in enumerate(Game.poss_cards):
                        deck = self._gen_deck(dc_idx, pc1_idx, pc2_idx)
                        d_val = self._dealer_turn(dc_val, deck)

                        if (d_val >= 21 or d_val < 0):
                            continue

                        self._player_turn(dc_val, d_val, pc1_val+pc2_val, deck)

    def _gen_deck(self, d_idx, p_idx1, p_idx2):
        # generate a random deck of cards; list of 13, each idx is the num cards left
        cards = [random.randint(0, self.decks*Game.suits) for _
                 in range(len(Game.poss_cards))]

        assert sum(cards) <= self.decks * Game.suits * 13
        # add additional possibilities for 10
        idx_10 = 8
        num_JQK = 3
        cards[idx_10] += random.randint(0, self.decks*Game.suits*num_JQK)


        # Less than required amount of cards for a game
        if sum(cards) < Game.min_cards:
            cards = _gen_deck(d_idx, p_idx1, p_idx2)

        if cards[d_idx] > 0:
            cards[d_idx] -= 1
        if cards[p_idx1] > 0:
            cards[p_idx1] -= 1
        if cards[p_idx2] > 0:
            cards[p_idx2] -= 1

        return cards

    def _dealer_turn(self, d_card, deck):
        assert d_card >= 2 and d_card <= 11
        d_val = d_card
        while d_val <= 17:
            next_card = self._get_card(deck)
            if next_card == -1:
                return next_card

            d_val += next_card

        return d_val

    def _player_turn(self, d_init_val, d_val, p_val, deck):
        curr_p_val = p_val
        # dealer has higher val than player -> hit
        while curr_p_val < d_val:
            self._save_data(1, d_init_val, p_val, deck)
            next_card = self._get_card(deck)
            if next_card == -1:
                return

            curr_p_val += next_card

        # check if player bust, if bust do nothing

        # player has won/tied and did not bust -> stand
        if p_val >= d_val and p_val <= 21:
            self._save_data(0, d_init_val, p_val, deck)


    def _get_card(self, deck):
        while sum(deck) > 0:
            card_idx = random.randint(0, len(Game.poss_cards)-1)
            if deck[card_idx] > 0:
                deck[card_idx] -= 1
                return card_idx + 2

        return -1

    def _save_data(self, hit_stand, d_val, p_val, deck):
        self.result.append(hit_stand)
        self.data += self._flatten(d_val, p_val, deck)

    def _flatten(self, *args):
        result = []
        for item in args:
            if isinstance(item, tuple) or isinstance(item, Iterable):
                result += [elem for elem in item]
            else:
                result.append(item)

        return result

