import random

from components import Hand, Deck
from enums import Outcome, Move


class DataGame():
    '''Creates data representing the odds of blackjack.'''

    def __init__(self, cards_in_deck, num_decks=6):
        assert cards_in_deck > 20

        self._create_deck(cards_in_deck, num_decks)
        self.valid_data = None
        self.player = None
        self.dealer = None

    def _create_deck(self, num_cards, num_decks):
        self.deck = Deck(num_decks)
        self.deck.shuffle()
        self.deck.set_total_cards(num_cards)

    def play(self, move):
        '''Run the possible outcome of the hands.'''
        self.valid_data = True
        cards_layout = self.deck.card_divide()
        dealer_init_val = self.dealer.value()
        player_val_pre_last_hit = self._play_round(move)
        if not self.valid_data:
            # busted before drawing last card
            return (Outcome.INVALID, 0, 0, 0, 0)

        player_aces = self.player.num_aces()
        win = self.outcome(self.player.value())

        return (win, dealer_init_val, player_val_pre_last_hit,
                player_aces, cards_layout)

    def reset_initial_cards(self):
        while len(self.player) > 2:
            self.player.remove_card()

        while len(self.dealer) > 1:
            self.dealer.remove_card()

    def deal_initial_cards(self):
        self.player = Hand()
        self._deal_card(self.player)
        self._deal_card(self.player)
        self.dealer = Hand()
        self._deal_card(self.dealer)

    def _remove_uninitial_cards(self):
        while (len(self.player) > 2):
            self.player.cards.pop()
        while (len(self.dealer) > 1):
            self.dealer.cards.pop()

    def _deal_card(self, hand):
        card = self.deck.next_card()
        hand.add_card(card)

    def _deal_card_copy(self, hand, deck_index):
        card = self.deck.card_at(deck_index)
        hand.add_card(card)

    def _play_round(self, move):
        post_cards_dealt = 0
        player_value = self.player.value()

        if move == Move.HIT:
            self._deal_card_copy(self.player, post_cards_dealt)
            post_cards_dealt += 1
        
        print("Player: {}".format(self.player))
        
        if player_value > 21:
            self.valid_data = False
            return

        self._dealer_turn(post_cards_dealt)
        print("Dealer: {}".format(self.dealer))
        return player_value

    def _bust(self, hand_value):
        '''Determine if the hand is worth more than 21.'''
        return hand_value > 21

    def _dealer_turn(self, post_cards_dealt):
        curr_deck_idx = post_cards_dealt
        while self.dealer.value() <= 17:
            self._deal_card_copy(self.dealer, curr_deck_idx)
            curr_deck_idx += 1

    def outcome(self, player_value):
        dealer_value = self.dealer.value()
        if self._bust(player_value):
            return Outcome.LOSS
        elif (player_value > dealer_value or self._bust(player_value)):
            return Outcome.WIN
        elif player_value == dealer_value:
            return Outcome.TIE
        else:
            return Outcome.LOSS
