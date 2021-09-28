""" assignment_5_james_beckwith
Blackjack / Twenty-one

Blackjack is a popular card game. The objective of the game is to draw cards
and obtain the highest total not exceeding 21.
Strictly speaking this is the game Twenty-one rather than Blackjack since the
program is not dealing with the true blackjack of Spades-Ace plus Jack of
Spades or Clubs

The program does not consider Double or Split rules of Blackjack, players may
tie with Dealer

The initial game setup provides for player options:
    Deal is from 1 to 8 standard 52 card decks
    From 1 to 5 players against Dealer
"""

import random
import sys

VALID_CHARS = set("abcdefghijklmnopqrstuvwxyz'-")
FACES = [("Ace", 11), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6),
    ("7", 7), ("8", 8), ("9", 9), ("10", 10), ("Jack", 10), ("Queen", 10),
    ("King", 10)]
SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
SUIT = 0    # Index constants for semantic access to playing card  fields
FACE = 1    #
VAL = 2     #

def get_input(prompt):
    try:
        field = input(f'{prompt}')
    except (KeyboardInterrupt, EOFError):
        print("Goodbye")
        sys.exit()
    except TypeError:
        print("Enter requested data")
        return ""
    else:
        parts = field.split()
        for part in parts:
            if set(part.casefold()) <= VALID_CHARS:
                return " ".join(parts)
            elif field.isnumeric:
                return field
            else:
                print('Invalid input, try again.')
                return ""

def valid_n_players():
    ans = get_input("How many players against dealer (1 to 5)")
    if set(ans) < set('12345'):
        return int(ans)
    print('Invalid selection, enter value 1 - 5')
    return 0

def valid_n_decks():
    ans = ""
    while not ans:
        ans = get_input("How many 52 card decks (1 to 8)")
    if set(ans) < set('12345678'):
        return int(ans)
    print('Invalid selection, enter value 1 - 8')
    return 0

def hit_stand():
    ans = ""
    while not ans:
        ans = get_input("\tHit or Stand (h|s)")
    if set(ans.casefold()) < set('hs'):
        return ans
    print('\tInvalid selection, enter an \'h\' or an \'s\'')
    return ""

def play_again():
    ans = ""
    while not ans:
        ans = get_input("\nDo you wish to play again?")
    if set(ans.casefold()) < set('yn'):
        return ans
    print('Invalid selection, enter a \'y\' or an \'n\'')
    return ""

def new_player(player_names):
    """ new_player(player_names)
    Parameters:
        player_names:   list of strings
    Keyboard input name of a player, validate and append to the
    'player_names' list
    """
    name = ""
    while not name:
        name = get_input("Enter player name: ")
        if not name:
            print("Name must not be empty, try again")
        else:
            parts = name.split()
            for part in parts:
                if set(part.casefold()) <= VALID_CHARS:
                    name = " ".join(parts)
                else:
                    print(">> Invalid characters in name, try again.")
                    name = ""
                if name.casefold() == 'dealer':
                    print("Name is already taken, use another.")
                    name = ""
    player_names.append(name)

def build_cards():
    """ build_cards()
    Initialize a list of 52 cards representing a standard playing card decks
    Create a list of cards from which to deal
        List will consist of 1 or moreu copies of the playing card decks
        when created, shuffle the list
    """
    def build_deck():
        ndx = 0
        deck = [("", "", 0)] * 52
        for i in SUITS:
            for j in FACES:
                deck[ndx] = (i, j[0], j[1])
                ndx += 1
        return deck
    deck = build_deck()
    cards = []
    for i in range(n_decks):
        cards.extend(deck)
    random.shuffle(cards)
    return cards

def hit(player,cards):
    """ hit(player,cards)
    Parameters:
        player  List of a given player's data record
        cards   list from which cards will be dealt
    Deal a card from the 'cards' list
    return a display string with a card's Suite and Face
    """
    card = cards.pop()
    player['hand'].append([card[SUIT],card[FACE]])
    player['total'] += card[VAL]
    if card[FACE] == "Ace":
        player['aceinhand'] = True
    return f'{card[SUIT]} {card[FACE]}'

def show_hand(player,cards):
    """ show_hand(player,cards)
    Parameters:
        player  List of a given player's data record
        cards   list from which cards will be dealt
    Build a display string showing the cards in a player's
    hand and the total value of the hand
    """
    hand = "\tCards: "
    for card in player['hand']:
        hand = f'{hand} |{card[0]}-{card[1]}| '
    print(f"{hand} total: {player['total']}")

def new_play(cards,player_names):
    """ new_play(cards,player_names)
    Parameters:
        cards   list from which cards will be dealt
        player_names    list containing the names of the players in this game

    This function will be called for each round of the game
    Deal the first 2 cards to each player and the dealer
    The second card of the dealer will be hidden until it is time for the dealer's
    hand to be played, when it will be shown in the display of the dealer's hand to
    After the initial 2-cards have been dealt to each player and the dealer, play will
    proceed for each player in succession, dealer last player

    After all players have played the winner will be proclaimed
    """
    high_player = ["",0]    # non-busted high player(s) name(s), high_score

    players = []    # initialize list with each player's data record
    for name in player_names:
        players.append({"name": name, "hand": [], "total": 0, "aceinhand": False})
    print(f"{'-'*80}")
    # Initial deal, 2 cards to each player, dealer's second card hidden
    dealt = ['first', 'second']
    for i in range(2):  # deal 2 cards to each player and the dealer
        print('\n')
        for player in reversed(players):
            card = hit(player, cards)   # the 'hit' function could be called 'deal'
            name = player['name']
            if name.casefold() == 'dealer' and i == 1:
                print(f'Dealer second card: Hidden')
            else:
                print(f'{name} {dealt[i]} card: {card}')

    # Now for each player
    for player in reversed(players):
        print('\n')     # a nice heading for each player's action
        name = player['name']
        print(f'{name} playing:')
        alive = True    # loop until player busts or stands
        while alive:
            show_hand(player,cards)
            if name == "Dealer":        # Dealer play is automatic
                if player['total'] < 17:
                    is_go = 'h'
                else:
                    is_go = 's'
            else:
                is_go = hit_stand()     # Get player's choice to hit or stand
                while not is_go:
                    is_go = hit_stand()

            if is_go == 'h':            # Deal another card to player
                card = hit(player,cards)
                print(f"\tDealt card {card}")
                if player['total'] > 21:        # Ace initial value is 11, if
                    if player['aceinhand']:     # hand would bust with an Ace,
                        player['aceinhand'] = False # but only once per Ace
                        player['total'] -= 10   # change Ace value to 1
                    else:
                        show_hand(player,cards)     # No luck, player busted
                        print(f"\t{name} busted!")
                        alive = False
            else:
                alive = False

        if player['total'] < 22:        # If a player has high score and not
            if player['total'] > high_player[1]:    # busted, update the
                high_player[0] = player['name']     # high-score tracking
                high_player[1] = player['total']    # structure
            elif player['total'] == high_player[1]:
                high_player[0] = f"tied: {high_player[0]}, {player['name']}"

    # All players have finished play, nicely format and print the winner(s)
    # information. Winners may be tied. If everyone busted, say so
    if high_player[1]:
        print(f"\nWinner is {high_player[0]} with total {high_player[1]}")
    else:
        print("\nThere are no winners")

if __name__ == '__main__':
    print("Welcome to Blackjack\n")

    # Set game configuration variables
    n_players = 0
    while n_players == 0:
        n_players = valid_n_players()
    n_decks = 0
    while n_decks == 0:
        n_decks = valid_n_decks()

    player_names = ["Dealer"]
    for i in range(n_players):
        # print(i,n_players,player_names)
        new_player(player_names)

    # build a randomized list from 1 to 8 standard playing card decks
    # we'll deal from this set of cards
    cards = build_cards()
    # i = 1
    # for card in cards:
    #     print(i,card)
    #     i += 1

    # Ask if player wants another round, loop until the answer is no
    more_play = 'y'
    while more_play == 'y':
        new_play(cards, player_names)
        more_play = ""
        while more_play == "":
            more_play = play_again()
