# Cards_Game
Simple Card Pair Game called as "JorPatti" in our native language.

## There are some basic rules to it:

1. 5 cards are shuffled among players (Eg 5 in this game)
2. The first person to create 3 pairs in its card set is the winner

## How to Play :

1. After giving 5 cards to each player, the remaining cards are kept in Middle and is called "Middle Deck".
2. First player picks card from "Middle Deck". Now he has 6 cards, and then checks if he has 3 pairs of card set with him,
   if yes then he is the winner, else he drops least interested card in middle, making it visible for others, to create a new deck called 
   "Open Deck".
3. Next Player has the option to pick card either from "Middle Deck"(cannot see card from this deck before hand) or from "Open Deck", to 
   make 3 pairs. After picking if he makes 3 pairs, then he is the winner, else he drops least interested card on top of "Open Deck" for 
   next player to choose from. And game goes on till one creates 3 pairs first.
4. If "Middle Deck" is finished, cards from "Open Deck" except of the top card, are shuffled and used as "Middle Deck".


## Techincal Details

1. Please build your own Django project first before making use of the code because
