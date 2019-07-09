import random

from .components import Hand, Deck
from .enum_outcome import Outcome


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

    def play(self, player_hits):
        '''Run the possible outcome of the hands.

        Args:
            player_hits: The number of times the player will hit.
        '''
        self.valid_data = True
        self._deal_initial_cards()
        cards_layout = self.deck.card_divide()
        dealer_init_val = self.dealer.value()
        player_val_pre_last_hit = self._play(player_hits)
        if not self.valid_data:
            # busted before drawing last card
            return (Outcome.INVALID, 0, 0, 0, 0)

        player_val_final = self.player.value()
        win = self._outcome()

        return (win, dealer_init_val, player_val_pre_last_hit,
                player_val_final, cards_layout)
    
    def play_without_initial_deals(self, player_hits):
        self.valid_data = True
        cards_layout = self.deck.card_divide()
        dealer_init_val = self.dealer.value()
        player_val_pre_last_hit = self._play(player_hits)
        if not self.valid_data:
            return False  # busted before drawing last card

        player_val_final = self.player.value()
        win = self._outcome()

        return (win, dealer_init_val, player_val_pre_last_hit,
                player_val_final, cards_layout)

    def _deal_initial_cards(self):
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

    def _play(self, player_hits):
        player_value_pre_last_hit = self._player_turn(player_hits)
        if self._bust(self.player):
            self.valid_data = False
            return

        self._dealer_turn(player_hits)

        return player_value_pre_last_hit

    def _player_turn(self, player_hits):
        '''Players turn to .

        Args:
            player_hits: The number of times the player will hit.
                         Must be greater than or equal to 0.
        '''
        assert player_hits >= 0
        if player_hits == 0:
            player_value_pre_last_hit = self.player.cards[0].value()

        for hit in range(player_hits):
            if hit == player_hits - 1:  # Value before last card dealt
                player_value_pre_last_hit = self.player.value()
            self._deal_card_copy(self.player, hit)

        return player_value_pre_last_hit

    def _bust(self, hand):
        '''Determine if the hand is worth more than 21.'''
        print(hand.value())
        return hand.value() > 21

    def _dealer_turn(self, player_hits):
        curr_deck_idx = player_hits
        while self.dealer.value() <= 17:
            self._deal_card_copy(self.dealer, curr_deck_idx)
            curr_deck_idx += 1

    def _outcome(self):
        if (self.player.value() > self.dealer.value() or
                self._bust(self.dealer)):
            return Outcome.WIN
        elif self.player.value() == self.dealer.value():
            return Outcome.TIE
        else:
            return Outcome.LOSS
