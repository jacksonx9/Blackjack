import random
import time

from .. import Player, BotPlayer, Hand, Deck


class Game():
    '''Controls the actions of the game'''

    def __init__(self, name, chips, num_decks=6):
        self.deck = Deck(num_decks)
        self.deck.shuffle()
        self.player = Player(name, chips)
        self.max_name_len = max(len(name), len('Dealer'))  # remove
        self.playing = False
        self.bot_players = list(BotPlayer(name) for name in ['Bot1', 'Bot2'])
        self.dealer = None

    def _deal_card(self, name, hand, announce=True):
        '''Take the next available card from deck and add to hand.'''
        card = self.deck.next_card()
        hand.add_card(card)
        if announce:
            time.sleep(1)
            prompt = 'dealt {}  {:>2} : {}'.format(card, hand.value(), hand)
            print(self.format_text(name, prompt))

    def _get_bet(self, minimum, multiple):
        '''Ask player for their bet and check constraints on answer.'''
        question = 'How much would you like to bet?'
        print()
        print(self.format_text(self.player.name, question.lower()))
        prompt = '{} available, {} minimum, multiples of {} only'.format(
            self.player.chips, minimum, multiple)
        print(self.format_text(self.player.name, prompt))
        bet = -1
        while bet < minimum or bet > self.player.chips or bet % multiple != 0:
            bet = input(self.format_text(
                self.player.name, 'enter amount ({}): '.format(minimum)))
            if bet == '':
                bet = minimum
            else:
                bet = int(bet)
        return bet

    def format_text(self, name, text):
        '''Prefix output with player's name.'''
        name = name.rjust(self.max_name_len)
        return '{} > {}'.format(name, text)

    def setup(self):
        '''Obtain bets and deal two cards to the player and the dealer.'''
        self.playing = True
        min_bet = 10

        bet = self._get_bet(min_bet, 2)
        self.player.bet(bet)
        self.player.hand = Hand(bet)
        self.dealer = Hand()
        for bot in self.bot_players:
            bot.hand = Hand()

        for _ in range(2):
            for bot in self.bot_players:
                self._deal_card(_, bot.hand, announce=False)
            self._deal_card(_, self.dealer, announce=False)
            self._deal_card(_, self.player.hand, announce=False)
        print()
        for bot in self.bot_players:
            prompt = 'hand dealt {:>2} : {}'.format(bot.hand.value(), bot.hand)
            print(self.format_text(bot.name, prompt))
        player_hand = self.player.hand
        print(self.format_text(self.player.name, 'hand dealt {:>2} : {}'
                               .format(player_hand.value(), player_hand)))
        print(self.format_text('Dealer', 'face up card  : {}'
                               .format(self.dealer.cards[0])))

    def check_for_blackjack(self):
        '''Check if blackjack and settle bets accordingly'''
        if self.dealer.blackjack():
            self.playing = False
            print()
            print(self.format_text('Dealer', 'scored blackjack : {}'
                                   .format(self.dealer)))
            if self.player.hand.value() == self.dealer.value():
                outcome = 'you scored blackjack as well.'
                self.player.push(self.player.hand.stake)
                print(self.format_text(self.player.name, outcome))
                return
        elif self.player.hand.blackjack():
            self.playing = False
            print(self.format_text(self.player.name, 'blackjack!'))
            self.settle_outcome()

    def settle_outcome(self):
        '''Decide the outcome of the player's hand compared to the dealer'''
        self.playing = False
        player_hand = self.player.hand
        if player_hand.value() > self.dealer.value() or self.dealer.bust():
            outcome = 'you beat the dealer! :)'
            self.player.win(player_hand.stake)
        elif player_hand.value() == self.dealer.value():
            outcome = 'you tied with the dealer :|'
            self.player.push(player_hand.stake)
        else:
            outcome = 'you lost to the dealer :('
        print(self.format_text(self.player.name, outcome))

    def hit(self, player, hand):
        '''Draw another card for player and determine outcome.'''
        self._deal_card(player.name, hand)

    def bust(self):
        '''Handle a player's hand that has busted.'''
        print(self.format_text(self.player.name, 'busted! :('))
        self.playing = False

    def dealer_turn(self):
        '''Controls dealer's turn and the outcome of the game.'''
        print()
        prompt = 'turns {}  {:>2} : {}'.format(
            self.dealer.cards[-1],
            self.dealer.value(),
            self.dealer)
        print(self.format_text('Dealer', prompt))
        while self.dealer.value() < 17:
            self._deal_card('Dealer', self.dealer)
        if self.dealer.bust():
            print(self.format_text('Dealer', 'busted!'))
        self.settle_outcome()

    def bots_turn(self):
        '''Controls bots' turn.'''
        for bot in self.bot_players:
            print()
            prompt = 'turns {}  {:>2} : {}'.format(
                bot.hand.cards[-1],
                bot.hand.value(),
                bot.hand)
            print(self.format_text(bot.name, prompt))
            while bot.hand.value() < 17:
                self._deal_card(bot.name, bot.hand)
            if bot.hand.bust():
                print(self.format_text(bot.name, 'busted!'))
            self.show_hand(bot.name, bot.hand)

    def show_hand(self, name, hand):
        '''Print player's current hand'''
        print()
        prompt = 'hand value {:>2} : {}'.format(hand.value(), hand)
        print(self.format_text(name, prompt))

    def play_hands(self):
        '''Play any active hands until completed'''
        if self.playing:
            self.bots_turn()
            self.play_hand(self.player.hand)
            if self.playing:
                self.dealer_turn()

    def play_hand(self, hand):
        '''Play the hand until finished'''
        self.show_hand(self.player.name, hand)

        while self.playing:
            if hand.twenty_one():
                print(self.format_text(self.player.name, 'scored 21! :)'))
                break
            if hand.bust():
                self.bust()
                break
            else:
                question = 'would you like to hit or stand? (H/s): '
                answers = ('H', 'S')

            prompt = self.format_text(self.player.name, question)
            resp = self.get_response(prompt, answers, default='H')
            if resp == 'H':
                if self.hit(self.player, hand):
                    break
            elif resp == 'S':
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

    def sufficient_cards(self):
        '''Determines if sufficient cards to play another round.'''
        return len(self.deck) > (len(self.bot_players) + 2) * 10
