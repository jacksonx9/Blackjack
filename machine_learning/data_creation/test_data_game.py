from unittest import TestCase

from .components import Card
from .data_game import DataGame, Hand, Outcome, Move


class DataGameTest(TestCase):
    def test_data_game_create_deck_whole_deck(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        self.assertEqual(whole_deck, len(game.deck))

    def test_data_game_create_deck_half_deck(self):
        half_deck = 52*3
        game = DataGame(half_deck)
        self.assertEqual(half_deck, len(game.deck))

    def test_data_game_play_player_bust(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.deal_initial_cards()
        while game.player.value() < 21:
            game._deal_card(game.player)
        (win, dealer_init_val, player_val_pre_last_hit, player_val_final,
            cards_layout) = game.play(Move.STAND)
        self.assertEqual(Outcome.INVALID, win)

    def test_data_game_play_player_win(self):
        pass  # nested while loops

    def test_data_game_deal_initial_cards(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.deal_initial_cards()
        self.assertEqual(whole_deck-3, len(game.deck))
        self.assertEqual(2, len(game.player))
        self.assertEqual(1, len(game.dealer))

    def test_data_game_deal_card(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game._deal_card(game.player)
        self.assertEqual(whole_deck-1, len(game.deck))
        self.assertEqual(1, len(game.player))

    def test_data_game_deal_card_copy(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game._deal_card_copy(game.player, 0)
        self.assertEqual(whole_deck, len(game.deck))
        self.assertEqual(1, len(game.player))

    def test_data_game_reset_initial_cards(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.deal_initial_cards()
        game._deal_card(game.player)
        game._deal_card(game.player)
        game._deal_card(game.dealer)
        game._deal_card(game.player)
        game.reset_initial_cards()
        self.assertEqual(2, len(game.player))
        self.assertEqual(1, len(game.dealer))

    def test_data_game_bust(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        while game.player.value() <= 21:
            self.assertFalse(game._bust(game.player.value()))
            game._deal_card(game.player)
        self.assertTrue(game._bust(game.player.value()))

    def test_data_game_dealer_turn(self):
        def cards_correct():
            for idx in range(player_hits):
                self.assertEqual(game.deck._cards.pop(0),
                                 game.player.cards[idx])
            num_cards_seen = len(game.dealer)
            for idx in range(num_cards_seen):
                self.assertEqual(game.deck._cards.pop(0),
                                 game.dealer.cards[idx])

        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game.dealer = Hand()
        player_hits = 1
        game._deal_card_copy(game.player, 0)
        game._dealer_turn(player_hits)
        self.assertEqual(whole_deck, len(game.deck))
        cards_correct()

    def test_data_game_outcome_player_bust(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game.dealer = Hand()
        player_card1 = Card("10")
        player_card2 = Card("10")
        player_card3 = Card("2")
        dealer_card = Card("2")
        game.player.add_card(player_card1)
        game.player.add_card(player_card2)
        game.player.add_card(player_card3)
        game.dealer.add_card(dealer_card)
        outcome = game.outcome(game.player.value())
        self.assertEqual(Outcome.LOSS, outcome)

    def test_data_game_outcome_win(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game.dealer = Hand()
        player_card = Card("3")
        dealer_card = Card("2")
        game.player.add_card(player_card)
        game.dealer.add_card(dealer_card)
        outcome = game.outcome(game.player.value())
        self.assertEqual(Outcome.WIN, outcome)

    def test_data_game_outcome_win_dealer_bust(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game.dealer = Hand()
        player_card = Card("3")
        dealer_card_1 = Card("10")
        dealer_card_2 = Card("10")
        dealer_card_3 = Card("2")
        game.player.add_card(player_card)
        game.dealer.add_card(dealer_card_1)
        game.dealer.add_card(dealer_card_2)
        game.dealer.add_card(dealer_card_3)
        outcome = game.outcome(game.player.value())
        self.assertEqual(Outcome.WIN, outcome)

    def test_data_game_outcome_tie(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game.dealer = Hand()
        player_card = Card("3")
        dealer_card = Card("3")
        game.player.add_card(player_card)
        game.dealer.add_card(dealer_card)
        outcome = game.outcome(game.player.value())
        self.assertEqual(Outcome.TIE, outcome)

    def test_data_game_outcome_loss(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game.dealer = Hand()
        player_card = Card("2")
        dealer_card = Card("3")
        game.player.add_card(player_card)
        game.dealer.add_card(dealer_card)
        outcome = game.outcome(game.player.value())
        self.assertEqual(Outcome.LOSS, outcome)
