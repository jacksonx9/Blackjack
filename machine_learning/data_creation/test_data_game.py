from unittest import TestCase

from .data_game import DataGame
from .components import Hand, Card
from .enum_outcome import Outcome


class DataGameTest(TestCase):
    def test_data_game_create_deck_whole_deck(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        self.assertEqual(whole_deck, len(game.deck))

    def test_data_game_create_deck_half_deck(self):
        half_deck = 52*3
        game = DataGame(half_deck)
        self.assertEqual(half_deck, len(game.deck))

    def test_data_game_play_round_player_bust(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        (win, dealer_init_val, player_val_pre_last_hit, player_val_final,
            cards_layout) = game.play(20)
        self.assertEqual(22, len(game.player))
        self.assertEqual(Outcome.INVALID, win)

    def test_data_game_play_round(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        (win, dealer_init_val, player_val_pre_last_hit, player_val_final,
            cards_layout) = game.play(0)
        self.assertEqual(game.player.cards[0].value(), player_val_pre_last_hit)
        self.assertEqual(2, len(game.player))

    def test_data_game_deal_initial_cards(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game._deal_initial_cards()
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

    def test_data_game_play_player_busted(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game.valid_data = True
        while game.player.value() <= 21:
            game._deal_card(game.player)
        game._play(1)
        self.assertFalse(game.valid_data)

    def test_data_game_play_valid_turn(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game.dealer = Hand()
        game.valid_data = True
        player_value_pre_last_hit = game._play(1)
        self.assertTrue(game.valid_data)
        self.assertEqual(0, player_value_pre_last_hit)
        self.assertGreater(game.dealer.value(), 0)

    def test_data_game_player_turn(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game._deal_card(game.player)
        expected_player_value_pre_last_hit = game.player.value()
        player_value_pre_last_hit = game._player_turn(1)
        self.assertEqual(whole_deck-1, len(game.deck))
        self.assertEqual(2, len(game.player))
        self.assertEqual(expected_player_value_pre_last_hit,
                         player_value_pre_last_hit)

    def test_data_game_bust(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        while game.player.value() <= 21:
            self.assertFalse(game._bust(game.player))
            game._deal_card(game.player)
        self.assertTrue(game._bust(game.player))

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

    def test_data_game_outcome_win(self):
        whole_deck = 52*6
        game = DataGame(whole_deck)
        game.player = Hand()
        game.dealer = Hand()
        player_card = Card("3")
        dealer_card = Card("2")
        game.player.add_card(player_card)
        game.dealer.add_card(dealer_card)
        outcome = game._outcome()
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
        outcome = game._outcome()
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
        outcome = game._outcome()
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
        outcome = game._outcome()
        self.assertEqual(Outcome.LOSS, outcome)
