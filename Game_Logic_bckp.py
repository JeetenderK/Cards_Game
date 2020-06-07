import pandas as pd
import os
import random
import numpy as np
import time
from datetime import datetime

def Number_Of_Pairs(player):
    pairs = []
    
    for Card in np.unique(player.Rank.values):
        count = np.count_nonzero(player.Rank.values == Card, axis=0)
        Number_of_pair = int(count/2)
        
        pairs.append((Card, Number_of_pair))
    
    return pairs


def Index_of_Random_Card_to_Drop(player):
    Options=[]

    for abc in Number_Of_Pairs(player):
        Indexes = player.index[player["Rank"] == abc[0]].tolist()
        if ((len(Indexes)) % 2) == 1:
            Options.append(random.choice(Indexes))

    #print("Available Index options to Drop : ", Options)
    Index_to_Drop = random.choice(Options)
    
    return Index_to_Drop


def if_Deck_finishes(Other_Deck):
    
    Card_on_top = Other_Deck.tail(1)
    Index_To_Drop = Card_on_top.index[0]
    Other_Deck = Other_Deck.drop(index = Index_To_Drop)
    
    Shuffled_Deck = Other_Deck.sample(frac=1)
    
    return Shuffled_Deck


def player_move_II(player_data, Middle_Deck_Remaining_Card_Set, Open_Deck):
    
    Target_Pairs = 3
    iternary = 0
    
    # If Middle Deck Finishes
    if len(Middle_Deck_Remaining_Card_Set) == 0:
        iternary += 1
        print(iternary, ". Card Counts :")
        print("   Remaining Cards in Middle Deck : ", len(Middle_Deck_Remaining_Card_Set))
        print("   Number of Cards in Open Deck : ", len(Open_Deck))
        iternary += 1
        print(iternary, ". Middle Deck is Empty... Time to take cards from Open deck... Taking..!!")
        
        Middle_Deck_Remaining_Card_Set = if_Deck_finishes(Open_Deck)
        Open_Deck = Open_Deck.tail(1)
        
        iternary += 1
        print(iternary, ". Now Card Counts :")
        print("   Remaining Cards in Middle Deck : ", len(Middle_Deck_Remaining_Card_Set))
        print("   Number of Cards in Open Deck : ", len(Open_Deck))
    
    
    player_char, player = player_data
    
    iternary += 1
    print(iternary, ". Player ", player_char,"'s turn ..")
    
    iternary += 1
    print(iternary, ". Player ",player_char," has below Deck before his turn :\n", player)
    
    Deck = ""

    # If Open Deck is Empty
    if Open_Deck.empty:
        
        Picked_Card_From_Middle_Deck = Middle_Deck_Remaining_Card_Set.sample(n=1, random_state = random.randint(0,100))
        Middle_Deck_Remaining_Card_Set = Middle_Deck_Remaining_Card_Set.drop(Picked_Card_From_Middle_Deck.index.values)
        
        iternary += 1
        print(iternary, ". Player ",player_char," Picked below Card From Middle Deck as Open Deck is empty:\n", Picked_Card_From_Middle_Deck)
        
        player = player.append(Picked_Card_From_Middle_Deck)
        Card_Pair_Count = Number_Of_Pairs(player)
        Number_Of_pairs = sum([i[1] for i in Card_Pair_Count])
        

        # Check if Player is winner ?        
        if Number_Of_pairs == Target_Pairs:
            iternary += 1
            print(iternary, ". if => if")
            
            return [True, player, Open_Deck, Picked_Card_From_Middle_Deck, None]
        else:
            
            # Automatic Selection to Drop a Card
            Index_To_Drop = Index_of_Random_Card_to_Drop(player)
            Card_To_Drop = player.loc[[Index_To_Drop]]
            player = player.drop(index = Index_To_Drop)
            
            iternary += 1
            print(iternary, ". Player ",player_char," has dropped below card :\n", Card_To_Drop)
            
            #Card_To_Drop_Having_index = Card_To_Drop.index.values[0]
            
            # Will append card at last of Open Deck
            Open_Deck.loc[Index_To_Drop] = pd.DataFrame([Card_To_Drop.loc[Index_To_Drop].tolist()], columns=["Rank", "Color"]).loc[0]
            
            iternary += 1
            print(iternary, ". Now Open Deck has this card on top :", Open_Deck.tail(1))
            
            Deck = "Middle"
            # Manual selection to Drop a Card
            """
            print(player)
            selection = int(input("Enter index of Card you want to drop ?"))
            if player.index.contains(selection):
                Open_Deck = Open_Deck.append(player.loc[[selection]])
                player = player.drop(index = selection)
            else:
                print("Invalid Index. Try again !!")
            """
    
    # If Open deck is not empty
    else:        
        
        iternary += 1
        print(iternary, ". Now Open Deck has this card on top :", Open_Deck.tail(1))
        
        
        #Check Open Deck for mathces
        Match_Found = Open_Deck.tail(1).Rank.values[0] in player.Rank.values
        
        if Match_Found:
            # If Match is found in Open Deck
            Picked_Card_From_Open_Deck = Open_Deck.tail(1)
            Open_Deck = Open_Deck[:-1]

            player = player.append(Picked_Card_From_Open_Deck)
            
            iternary += 1
            print(iternary, ". Player ",player_char," Picked below Card From Open Deck :\n", Picked_Card_From_Open_Deck)
            
            # Find Pairs in your Deck
            Card_Pair_Count = Number_Of_Pairs(player)
            Number_Of_pairs = sum([i[1] for i in Card_Pair_Count])
            
            Open = Open_Deck.tail(1)

            # Check if Player is winner ?        
            if Number_Of_pairs == Target_Pairs:
                iternary += 1
                print(iternary, ". else => if => if")

                return [True, player, Open, Picked_Card_From_Open_Deck, None]
            else:
            # if not winner then drop a card
            
                # Automatic Selection to Drop a Card
                Index_To_Drop = Index_of_Random_Card_to_Drop(player)
                Card_To_Drop = player.loc[[Index_To_Drop]]
                player = player.drop(index = Index_To_Drop)

                # Will append card at last of Open Deck
                Open_Deck.loc[Index_To_Drop] = pd.DataFrame([Card_To_Drop.loc[Index_To_Drop].tolist()], columns=["Rank", "Color"]).loc[0]
                
                
                iternary += 1
                print(iternary, ". Now Open Deck has this card on top :", Open_Deck.tail(1))
                Deck = "Open"
        else :
            
            # If No matches are found in Open Deck go for card from Middle Deck
            
            # Pick Card from Middle Deck
            Picked_Card_From_Middle_Deck = Middle_Deck_Remaining_Card_Set.sample(n=1, random_state = random.randint(0,100))
            Middle_Deck_Remaining_Card_Set = Middle_Deck_Remaining_Card_Set.drop(Picked_Card_From_Middle_Deck.index.values)

            player = player.append(Picked_Card_From_Middle_Deck)
            
            iternary += 1
            print(iternary, ". Player ",player_char," Picked below Card From Middle Deck :\n", Picked_Card_From_Middle_Deck)
            
            # Find Pairs in your Deck
            Card_Pair_Count = Number_Of_Pairs(player)
            Number_Of_pairs = sum([i[1] for i in Card_Pair_Count])

            Open = Open_Deck.tail(1)

            # Check if Player is winner ?        
            if Number_Of_pairs == Target_Pairs:
                iternary += 1
                print(iternary, ". else => else => if")
                
                return [True, player, Open, Picked_Card_From_Middle_Deck, None]
            else:
            # if not winner then drop a card
            
                # Automatic Selection to Drop a Card
                Index_To_Drop = Index_of_Random_Card_to_Drop(player)
                Card_To_Drop = player.loc[[Index_To_Drop]]
                player = player.drop(index = Index_To_Drop)

                # Will append card at last of Open Deck
                Open_Deck.loc[Index_To_Drop] = pd.DataFrame([Card_To_Drop.loc[Index_To_Drop].tolist()], columns=["Rank", "Color"]).loc[0]
                
                iternary += 1
                print(iternary, ". Now Open Deck has this card on top :", Open_Deck.tail(1))
                Deck = "Middle"
    
    iternary += 1
    print(iternary, ". Player ",player_char," has below Deck after his turn:\n")
    
    Open = Open_Deck.tail(1)
    if Deck == "Middle" :
        Card_Picked = Picked_Card_From_Middle_Deck
    else :
        Card_Picked = Picked_Card_From_Open_Deck

    return [False, player, Open, Card_Picked, Card_To_Drop]



'''Remaining_Card_Set = pd.read_csv(os.path.abspath(os.getcwd() + '/../Cards.csv'), index_col="Index")
Number_of_players = 5
Number_of_Cards_per_player = 5
Players = ["A","B","C","D","E"]

A = Remaining_Card_Set.sample(n= Number_of_Cards_per_player, random_state = random.randint(0,100))
Remaining_Card_Set = Remaining_Card_Set.drop(A.index.values)

B = Remaining_Card_Set.sample(n=Number_of_Cards_per_player, random_state = random.randint(0,100))
Remaining_Card_Set = Remaining_Card_Set.drop(B.index.values)

C = Remaining_Card_Set.sample(n=Number_of_Cards_per_player, random_state = random.randint(0,100))
Remaining_Card_Set = Remaining_Card_Set.drop(C.index.values)

D = Remaining_Card_Set.sample(n=Number_of_Cards_per_player, random_state = random.randint(0,100))
Remaining_Card_Set = Remaining_Card_Set.drop(D.index.values)

E = Remaining_Card_Set.sample(n=Number_of_Cards_per_player, random_state = random.randint(0,100))
Remaining_Card_Set = Remaining_Card_Set.drop(E.index.values)

Middle_Deck_Remaining_Card_Set = Remaining_Card_Set
Open_Deck = pd.DataFrame(columns=["Rank", "Color"])

print(Open_Deck)

Number_of_Rounds = 0

Time_now = datetime.now().strftime("%d/%m/%Y - %H:%M:%S.%f")
print("Game Started at : ", Time_now)

while(1):
    
    A_Is_Winner, A = player_move_II(["A", A])
    print(A)
    
    if A_Is_Winner:
        print("Player A is Winner")
        break
    print("\n")
    
    
    B_Is_Winner, B = player_move_II(["B", B])
    print(B)
    
    if B_Is_Winner:
        print("Player B is Winner")
        break
    print("\n")
    
    
    C_Is_Winner, C = player_move_II(["C", C])
    print(C)
    
    if C_Is_Winner:
        print("Player C is Winner")
        break
    print("\n")
    
    
    D_Is_Winner, D = player_move_II(["D", D])
    print(D)
    
    if D_Is_Winner:
        print("Player D is Winner")
        break
    print("\n")
    
    
    E_Is_Winner, E = player_move_II(["E", E])
    print(E)
    
    if E_Is_Winner:
        print("Player E is Winner")
        break
    print("\n")
    
    Time_now = datetime.now().strftime("%d/%m/%Y - %H:%M:%S.%f")
    Number_of_Rounds += 1
    
    print("\n")
    print("<------------ Game Stats ------------->")
    print("Remaining Cards in Middle Deck : ", len(Middle_Deck_Remaining_Card_Set))
    print("Number of Cards in Open Deck : ", len(Open_Deck))
    print("Rounds complete : ", Number_of_Rounds)
    print("Round Completed at : ", Time_now)
    print("<------------ Game Stats ------------->")
    print("\n")

Time_now = datetime.now().strftime("%d/%m/%Y - %H:%M:%S.%f")
print("\n")
print("<------------ Game Stats ------------->")
print("Remaining Cards in Middle Deck : ", len(Middle_Deck_Remaining_Card_Set))
print("Number of Cards in Open Deck : ", len(Open_Deck))
print("Total Rounds Played : ", Number_of_Rounds)
print("Game Ended at : ", Time_now)
print("<------------ Game Stats ------------->")
print("\n")

'''