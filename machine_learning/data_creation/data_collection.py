from game.blackjack.game.game import Game


class DataCollection():  # https://docs.scipy.org/doc/scipy/reference/tutorial/io.html
    def __init__(self):
        game = Game('Player', 1000)

    def setup(self):
        pass

    def play_round(self, rounds):
        for _ in rounds:
            if not self.game.player.has_chips(10):
                print('No one with any chips remaining - game over')
                break
            if not self.game.sufficient_cards():
                print('Insufficent card. Play another game.')
                break
            self.game.setup()
            self.game.check_for_blackjack()
            self.game.play_hands()

    def _try_all_options(self):
        pass

    def _reset_cards(self):
        pass

    def _create_mat_file(self):
        pass

    def _add_data_to_mat_file(self, data):
        # sort data
        # hand value, has ace
        pass

    def _player_hand_value(self):
        hand = self.game.player.hand

    def _player_number_of_aces(self):
        hand = self.game.player.hand

    def _remaining_cards(self):
        deck = self.game.deck
        # number of cards for each value

    def _loading_bar(self):
        pass
