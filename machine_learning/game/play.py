from blackjack.game.game import Game


def get_response(question, accepted, default):
    '''Get input that matches the accepted answers'''
    while True:
        resp = input(question).upper()
        if resp == '':
            resp = default
        if resp in accepted:
            break
    return resp

def start_game():
    '''Obtain player names and starting chips'''
    number_players = 6
    while True:
        prompt = 'Enter up to 6 player names or return for single player game: '
        names = input(prompt.format(number_players))
        if names == '':
            names = ['Player']
        else:
            names = names.split(' ')
        if len(names) > number_players:
            print('Maximum of 6 players only please!'.format(number_players))
        else:
            break

    print()
    chips = input('Enter starting number of chips (100): ')
    if chips == '':
        chips = 100
    else:
        chips = int(chips)
    return Game(names, chips)

def main():
    '''Run the main game loop'''
    try:
        print()
        game = start_game()

        while True:
            if not game.players_with_chips(10):
                print('No one with any chips remaining - game over')
                break
            game.setup()
            game.check_for_dealer_blackjack()
            # bots check for blackjack
            game.check_for_player_blackjack()
            # bots play hands
            game.play_hands()

    except KeyboardInterrupt:
        print()
    finally:
        if game:
            game.results()
        print()
        print('Thanks for playing.')
        print()


if __name__ == '__main__':
    main()