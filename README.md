# blackjack / Twenty-one

Blackjack is a popular card game. The objective of the game is to draw cards and obtain the highest total not exceeding 21.
Strictly speaking this is the game Twenty-one rather than Blackjack since the program is
is not dealing with the true blackjack of Spades-Ace plus Jack of Spades or Clubs

The program does not consider Double or Split rules of Blackjack, players may tie with Dealer.
A hand containing an Ace will count that card as having value==1 if the hand would otherwise
bust if value==10. If the hand total value<=21 with an Ace value==10, the card retains its
value.

The initial game setup provides for player options:
    Deal is from 1 to 8 standard 52 card decks
    From 1 to 5 players against Dealer

To run the script:
    $ python3 blackjack.py
