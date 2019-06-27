from blackjack.game.game import Game


def start_game():
    '''Obtain player names and starting chips'''
    number_players = 6

    prompt = 'Please enter your name (default is "Player"): '
    name = input(prompt)
    if name == '':
        name = 'Player'  # Remove these prints later

    chips = 1000
    return Game(name, chips)


def main():
    '''Run the main game loop'''
    try:
        print()
        game = start_game()

        while True:
            if not game.player.has_chips(10):
                print('No one with any chips remaining - game over')
                break
            game.setup()
            game.check_for_blackjack()
            # bots play hands
            game.play_hands()

    except KeyboardInterrupt:
        print()
    finally:
        print('Thanks for playing.')
        print()

if __name__ == '__main__':
    main()
