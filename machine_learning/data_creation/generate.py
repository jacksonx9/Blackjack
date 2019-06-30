from game.blackjack.game.game import Game


def start_game():
    '''Obtain player name and starting chips.'''
    prompt = 'Please enter your name (default is "Player"): '
    name = input(prompt)
    if name == '':
        name = 'Player'

    chips = 1000
    return Game(name, chips)


def main():
    '''Run the main game loop.'''
    try:
        print()
        game = start_game()

        while True:
            if not game.player.has_chips(10):
                print('No one with any chips remaining - game over')
                break
            if not game.sufficient_cards():
                print('Insufficent card. Play another game.')
                break
            game.setup()
            game.check_for_blackjack()
            game.play_hands()

    except KeyboardInterrupt:
        print()
    finally:
        print('Thanks for playing.')
        print()


if __name__ == '__main__':
    main()
