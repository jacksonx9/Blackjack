from blackjack.game.game import Game
from blackjack.person.person import PLAYER_COLORS

MAX_PLAYERS = len(PLAYER_COLORS)

def clear_screen():
    '''Clear the screen for better view'''
    print('\033[H\033[J')

def continue_prompt():
    '''Clear the screen before starting a new round'''
    print()
    input('Hit enter to continue - ctrl-c to exit: ')
    clear_screen()

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
    while True:
        prompt = 'Enter up to {} player names or return for single player game: '
        names = input(prompt.format(MAX_PLAYERS))
        if names == '':
            names = ['Player']
        else:
            names = names.split(' ')
        if len(names) > MAX_PLAYERS:
            print('Maximum of {} players only please!'.format(MAX_PLAYERS))
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
    clear_screen()
    print('''
          Welcome to Blackjack!
          ---------------------
This is the gambling game also known as 21
where you and others can play against the
computer dealer.
There is one 52 pack of cards in the deck
and the rules are documented here*. Purely
for fun, the game tracks your results and
and reports them at the conclusion.
* https://en.wikipedia.org/wiki/Blackjack
    ''')
    try:
        print()
        game = start_game()

        while True:
            continue_prompt()
            if not game.players_with_chips(10):
                print('No one with any chips remaining - game over')
                break
            game.setup()
            game.offer_insurance()
            game.check_for_dealer_blackjack()
            game.check_for_player_blackjack()
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