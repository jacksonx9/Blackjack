import random
import time
from termcolor import colored

from ..person.person import PLAYER_COLORS
from ..person import Player
from ..hand.hand import Hand
from ..deck.deck import Deck


class Game():
    '''Controls the actions of the game'''

    def __init__(self, names, chips):
        self.deck = Deck()
        self.deck.shuffle()
        self.colors = list(PLAYER_COLORS)
        self.players = list(Player(name, chips, self.__get_color())
                            for name in names)
        self.max_name_len = max(max(len(name)
                                    for name in names), len('Dealer'))
        self.playing = False
        self.dealer = None

    def __get_color(self):
        '''Obtain a random color from available termcolors.'''
        assert self.colors
        colors = self.colors
        color = random.choice(colors)
        colors.remove(color)
        return color

    def _deal_card(self, name, hand, color='white', announce=True):
        '''Take the next available card from deck and add to hand.'''
        card = self.deck.next_card()
        hand.add_card(card)
        if announce:
            time.sleep(1)
            prompt = 'dealt {}  {:>2} : {}'.format(card, hand.value(), hand)
            print(self.format_text(name, prompt, color))

    def _get_bet(self, player, question, minimum, multiple):
        '''Ask player for their bet and check constraints on answer.'''
        print()
        print(self.format_text(player.name, question.lower(), player.color))
        prompt = '{} available, {} minimum, multiples of {} only'.format(
            player.chips, minimum, multiple)
        print(self.format_text(player.name, prompt, player.color))
        bet = -1
        while bet < minimum or bet > player.chips or bet % multiple != 0:
            bet = input(self.format_text(
                player.name, 'enter amount ({}): '.format(minimum),
                player.color))
            if bet == '':
                bet = minimum
            else:
                try:
                    bet = int(bet)
                except ValueError:
                    pass
        return bet

    def format_text(self, name, text, color='white'):
        '''Prefix output with player's name and colorize'''
        name = name.rjust(self.max_name_len)
        return colored('{} > {}'.format(name, text), color)

    def players_with_chips(self, min=1):
        '''Returns a list of players with chips remaining'''
        return list(p for p in self.players if p.has_chips(min))

    def active_players(self):
        '''Generator of layers with active hands'''
        for player in self.players:
            if player.has_active_hands():
                yield player

    def has_active_hands(self):
        '''Are there any active hands remaining?'''
        return list(p for p in self.players if p.has_active_hands())

    def setup(self):
        '''Obtain bets and deal two cards to the player and the dealer.'''
        hands = []
        self.playing = True
        min_bet = 10
        random.shuffle(self.players)  # change to ai_players first then player
        players = self.players_with_chips(min_bet)
        if not players:
            return

        for player in players:
            player.insurance = 0
            bet = self._get_bet(player, 'How much would you like to bet?',
                                min_bet, 2)
            hand = Hand(bet)
            hands.append(hand)
            player.bet(bet)
            player.hands = [hand]

        dealer = Hand(0)
        for _ in range(2):
            for hand in hands:
                self._deal_card(_, hand, announce=False)
            self._deal_card(_, dealer, announce=False)
        print()
        for player in players:
            hand = player.hands[0]
            prompt = 'hand dealt {:>2} : {}'.format(hand.value(), hand)
            print(self.format_text(player.name, prompt, player.color))
        print(self.format_text(
            'Dealer', 'face up card  : {}'.format(dealer.cards[0])))
        self.dealer = dealer

    def check_for_dealer_blackjack(self):
        '''Check if dealer has blackjack and settle bets accordingly'''
        dealer = self.dealer
        players = self.active_players()
        if dealer.blackjack():
            self.playing = False
            print()
            print(self.format_text('Dealer', 'scored blackjack : {}'
                                   .format(dealer)))
            for player in players:
                for hand in player.active_hands():
                    if hand.value() == dealer.value():
                        outcome = 'you scored blackjack as well.'
                        player.push(hand.stake)
                        print(self.format_text(
                            player.name, outcome, player.color))

    def check_for_player_blackjack(self):
        '''Check if any player has blackjack and settle bets accordingly'''
        dealer = self.dealer
        players = self.active_players()
        for player in players:
            for hand in player.active_hands():
                if hand.blackjack():
                    print(self.format_text(player.name, 'you scored blackjack!',
                                           player.color))
                    self.settle_outcome(dealer, player, hand)

    def settle_outcome(self, dealer, player, hand):
        '''Decide the outcome of the player's hand compared to the dealer'''
        hand.active = False
        if hand.value() > dealer.value() or dealer.bust():
            outcome = 'you beat the dealer! :)'
            if hand.blackjack():
                odds = 1.5
            else:
                odds = 1
            player.win(hand.stake, odds)
        elif hand.value() == dealer.value():
            outcome = 'you tied with the dealer :|'
            player.push(hand.stake)
        else:
            outcome = 'you lost to the dealer :('
            player.loss()
        print(self.format_text(player.name, outcome, player.color))

    def split_hand(self, player, hand):
        '''Split player's hand if possible'''
        if hand.pair() and player.has_chips(hand.stake):
            prompt = 'would you like to split your pair? (Y/n): '
            prompt = self.format_text(player.name, prompt, player.color)
            resp = self.get_response(prompt, ('Y', 'N'), 'Y')
            if resp == 'Y':
                new_hand = hand.split()
                player.bet(hand.stake)
                self._deal_card(player.name, hand, player.color)
                self._deal_card(player.name, new_hand, player.color)
                player.hands.append(new_hand)
                self.show_hand(player.name, hand, player.color)

    def hit(self, player, hand):
        '''Draw another card for player and determine outcome.'''
        self._deal_card(player.name, hand, player.color)

    def bust(self, player, hand):
        '''Handle a player's hand that has busted.'''
        print(self.format_text(player.name, 'busted! :(', player.color))
        player.loss()
        hand.active = False

    def double_down(self, player, hand):
        '''Player wishes to double their bet and receive one more card.'''
        player.bet(hand.stake)
        hand.stake += hand.stake
        self._deal_card(player.name, hand, player.color)
        if hand.bust():
            self.bust(player, hand)

    def dealer_turn(self):
        '''Controls dealer's turn and the outcome of the game.'''
        dealer = self.dealer
        print()
        prompt = 'turns {}  {:>2} : {}'.format(
            dealer.cards[-1],
            dealer.value(),
            dealer)
        print(self.format_text('Dealer', prompt))
        while dealer.value() < 17:
            self._deal_card('Dealer', dealer)
        if dealer.bust():
            print(self.format_text('Dealer', 'busted!'))
        for player in self.active_players():
            for hand in player.active_hands():
                self.settle_outcome(dealer, player, hand)

    def results(self):
        '''Print player statistics'''
        print()
        players = sorted(self.players,
                         reverse=True,
                         key=lambda x: (x.chips,
                                        x.results['wins']*3 +
                                        x.results['ties'],
                                        -x.results['losses']))
        for player in players:
            results = ',  '.join('{}: {:>2}'.format(k, v) for k, v in
                                 player.results.items())
            prompt = 'chips: {:>3},  {}'.format(player.chips, results)
            print(self.format_text(player.name, prompt, player.color))

    def show_hand(self, name, hand, color='white'):
        '''Print player's current hand'''
        print()
        prompt = 'hand value {:>2} : {}'.format(hand.value(), hand)
        print(self.format_text(name, prompt, color))

    def play_hands(self):
        '''Play any active hands until completed'''
        if self.playing:
            for player in self.active_players():
                for hand in player.active_hands():
                    self.play_hand(player, hand)
            if self.has_active_hands():
                self.dealer_turn()

    def play_hand(self, player, hand):
        '''Play the hand until finished'''
        self.show_hand(player.name, hand, player.color)
        if player.can_split(hand):
            self.split_hand(player, hand)

        while hand.active:
            if hand.twenty_one():
                print(self.format_text(player.name, 'scored 21! :)',
                                       player.color))
                break
            if hand.bust():
                self.bust(player, hand)
                break
            if player.can_double_down(hand):
                question = 'would you like to hit, stand or double down? (H/s/d): '
                answers = ('H', 'S', 'D')
            else:
                question = 'would you like to hit or stand? (H/s): '
                answers = ('H', 'S')

            prompt = self.format_text(player.name, question, player.color)
            resp = self.get_response(prompt, answers, default='H')
            if resp == 'H':
                if self.hit(player, hand):
                    break
            elif resp == 'S':
                break
            elif resp == 'D':
                self.double_down(player, hand)
                break
            else:
                # should never get here!
                raise ValueError

    def get_response(self, question, accepted, default):
        '''Get input that matches the accepted answers'''
        while True:
            resp = input(question).upper()
            if resp == '':
                resp = default
            if resp in accepted:
                break
        return resp
