import asyncio
from channels.consumer import AsyncConsumer
import json
import pandas as pd
import os
import random
import numpy as np


class Global_Variables:
    global Open_Deck
    global Middle_Deck_Remaining_Card_Set
    Middle_Deck_Finish_Count = 0


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
    
    Global_Variables.Middle_Deck_Remaining_Card_Set = Other_Deck.sample(frac=1)


def player_move_II(player_data):
    
    Target_Pairs = 3
    iternary = 0
    Text = ""

    # If Middle Deck Finishes
    if len(Global_Variables.Middle_Deck_Remaining_Card_Set) == 0:
        iternary += 1
        #print(iternary, ". Card Counts :")
        Text += str(iternary) + ". Card Counts : \n"
        Text += "  Remaining Cards in Middle Deck : " + str(len(Global_Variables.Middle_Deck_Remaining_Card_Set)) + "\n" 
        #print("   Number of Cards in Open Deck : ", len(Global_Variables.Open_Deck))
        Text += "  Number of Cards in Open Deck : " + str(len(Global_Variables.Open_Deck)) + "\n" 
        iternary += 1
        Text += str(iternary) + ". Middle Deck is Empty... Time to take cards from Open deck... Taking..!!" + "\n" 
        Global_Variables.Middle_Deck_Finish_Count = Global_Variables.Middle_Deck_Finish_Count + 1
        if_Deck_finishes(Global_Variables.Open_Deck)
        Global_Variables.Open_Deck = Global_Variables.Open_Deck.tail(1)
        
        iternary += 1
        #print(iternary, ". Now Card Counts :")
        #print("   Remaining Cards in Middle Deck : ", len(Global_Variables.Middle_Deck_Remaining_Card_Set))
        #print("   Number of Cards in Open Deck : ", len(Global_Variables.Open_Deck))
        Text += str(iternary) + ". Now Card Counts :" + "\n"
        Text += "   Remaining Cards in Middle Deck : " + str(len(Global_Variables.Middle_Deck_Remaining_Card_Set)) + "\n"
        Text += "   Number of Cards in Open Deck : ", str(len(Global_Variables.Open_Deck)) + "\n"

    player_char, player = player_data
    
    iternary += 1
    Text += str(iternary) + ". Player " + str(player_char) +"'s turn .." + "\n"
    
    iternary += 1
    Text += str(iternary) + ". Player " + str(player_char) + " has below Deck before his turn :\n" + player.to_string() + "\n"
    
    Deck = ""

    # If Open Deck is Empty
    if Global_Variables.Open_Deck.empty:
        
        Picked_Card_From_Middle_Deck = Global_Variables.Middle_Deck_Remaining_Card_Set.sample(n=1, random_state = random.randint(0,100))
        Global_Variables.Middle_Deck_Remaining_Card_Set = Global_Variables.Middle_Deck_Remaining_Card_Set.drop(Picked_Card_From_Middle_Deck.index.values)
        
        iternary += 1
        Text += str(iternary) + ". Player " + str(player_char) + " Picked below Card From Middle Deck as Open Deck is empty:\n" + Picked_Card_From_Middle_Deck.to_string() + "\n"
        
        player = player.append(Picked_Card_From_Middle_Deck)
        Card_Pair_Count = Number_Of_Pairs(player)
        Number_Of_pairs = sum([i[1] for i in Card_Pair_Count])
        

        # Check if Player is winner ?        
        if Number_Of_pairs == Target_Pairs:
            iternary += 1
            Text += str(iternary) + ". if => if"
            
            return [True, player, Global_Variables.Open_Deck, Picked_Card_From_Middle_Deck, None, Text]
        else:
            
            # Automatic Selection to Drop a Card
            Index_To_Drop = Index_of_Random_Card_to_Drop(player)
            Card_To_Drop = player.loc[[Index_To_Drop]]
            player = player.drop(index = Index_To_Drop)
            
            iternary += 1
            Text += str(iternary) + ". Player " + str(player_char) + " has dropped below card :\n" + Card_To_Drop.to_string() + "\n"
            
            #Card_To_Drop_Having_index = Card_To_Drop.index.values[0]
            
            # Will append card at last of Open Deck
            Global_Variables.Open_Deck.loc[Index_To_Drop] = pd.DataFrame([Card_To_Drop.loc[Index_To_Drop].tolist()], columns=["Rank", "Color"]).loc[0]
            
            iternary += 1
            Text += str(iternary) + ". Now Open Deck has this card on top :" + Global_Variables.Open_Deck.tail(1).to_string() + "\n"
            
            Deck = "Middle"
    
    # If Open deck is not empty
    else:        
        
        iternary += 1
        Text += str(iternary) + ". Now Open Deck has this card on top :" + Global_Variables.Open_Deck.tail(1).to_string() + "\n"
        
        
        #Check Open Deck for mathces
        Match_Found = Global_Variables.Open_Deck.tail(1).Rank.values[0] in player.Rank.values
        
        if Match_Found:
            # If Match is found in Open Deck
            Picked_Card_From_Open_Deck = Global_Variables.Open_Deck.tail(1)
            Global_Variables.Open_Deck = Global_Variables.Open_Deck[:-1]

            player = player.append(Picked_Card_From_Open_Deck)
            
            iternary += 1
            Text += str(iternary) + ". Player " + str(player_char) + " Picked below Card From Open Deck :\n" + Picked_Card_From_Open_Deck.to_string() + "\n"
            
            # Find Pairs in your Deck
            Card_Pair_Count = Number_Of_Pairs(player)
            Number_Of_pairs = sum([i[1] for i in Card_Pair_Count])
            
            Open = Global_Variables.Open_Deck.tail(1)

            # Check if Player is winner ?        
            if Number_Of_pairs == Target_Pairs:
                iternary += 1
                Text += str(iternary) + ". else => if => if"

                return [True, player, Open, Picked_Card_From_Open_Deck, None, Text]
            else:
            # if not winner then drop a card
            
                # Automatic Selection to Drop a Card
                Index_To_Drop = Index_of_Random_Card_to_Drop(player)
                Card_To_Drop = player.loc[[Index_To_Drop]]
                player = player.drop(index = Index_To_Drop)

                # Will append card at last of Open Deck
                Global_Variables.Open_Deck.loc[Index_To_Drop] = pd.DataFrame([Card_To_Drop.loc[Index_To_Drop].tolist()], columns=["Rank", "Color"]).loc[0]
                
                
                iternary += 1
                Text += str(iternary) + ". Now Open Deck has this card on top :" + Global_Variables.Open_Deck.tail(1).to_string() + "\n"
                Deck = "Open"
        else :
            
            # If No matches are found in Open Deck go for card from Middle Deck
            
            # Pick Card from Middle Deck
            Picked_Card_From_Middle_Deck = Global_Variables.Middle_Deck_Remaining_Card_Set.sample(n=1, random_state = random.randint(0,100))
            Global_Variables.Middle_Deck_Remaining_Card_Set = Global_Variables.Middle_Deck_Remaining_Card_Set.drop(Picked_Card_From_Middle_Deck.index.values)

            player = player.append(Picked_Card_From_Middle_Deck)
            
            iternary += 1
            Text += str(iternary) + ". Player " + str(player_char) + " Picked below Card From Middle Deck :\n" + Picked_Card_From_Middle_Deck.to_string() + "\n"
            
            # Find Pairs in your Deck
            Card_Pair_Count = Number_Of_Pairs(player)
            Number_Of_pairs = sum([i[1] for i in Card_Pair_Count])

            Open = Global_Variables.Open_Deck.tail(1)

            # Check if Player is winner ?        
            if Number_Of_pairs == Target_Pairs:
                iternary += 1
                Text += str(iternary) + ". else => else => if"
                
                return [True, player, Open, Picked_Card_From_Middle_Deck, None, Text]
            else:
            # if not winner then drop a card
            
                # Automatic Selection to Drop a Card
                Index_To_Drop = Index_of_Random_Card_to_Drop(player)
                Card_To_Drop = player.loc[[Index_To_Drop]]
                player = player.drop(index = Index_To_Drop)

                # Will append card at last of Open Deck
                Global_Variables.Open_Deck.loc[Index_To_Drop] = pd.DataFrame([Card_To_Drop.loc[Index_To_Drop].tolist()], columns=["Rank", "Color"]).loc[0]
                
                iternary += 1
                Text += str(iternary) + ". Now Open Deck has this card on top :" + Global_Variables.Open_Deck.tail(1).to_string() + "\n"
                Deck = "Middle"
    
    iternary += 1
    Text += str(iternary) + ". Player " + str(player_char) + " has below Deck after his turn:\n" + player.to_string() + "\n"
    
    Open = Global_Variables.Open_Deck.tail(1)
    if Deck == "Middle" :
        Card_Picked = Picked_Card_From_Middle_Deck
    else :
        Card_Picked = Picked_Card_From_Open_Deck

    return [False, player, Open, Card_Picked, Card_To_Drop, Text]



class JorPatti_WebAppConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)

        await self.send({
            "type":"websocket.accept"
        })
        

        sleep_time = 2
        No_of_Rounds = 0
        Remaining_Card_Set = pd.read_csv(os.path.abspath(os.getcwd() + '/../Cards.csv'), index_col="Index")
        Number_of_Cards_per_player = 5

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

        Global_Variables.Middle_Deck_Remaining_Card_Set = Remaining_Card_Set
        Global_Variables.Open_Deck = pd.DataFrame(columns=["Rank", "Color"])
        

        
        arr_symbol = ['A', 'B', 'C', 'D', 'E']
        arr_variable = [A, B, C, D, E]

        arr = list(zip(arr_symbol, arr_variable))

        '''arrC = ['A', 'B', 'C', 'D', 'E', 'Middle', 'Open']
        arrV = [A, B, C, D, E, Global_Variables.Middle_Deck_Remaining_Card_Set, Global_Variables.Open_Deck]'''

        while(1):

            for Player in arr :

                Is_Winner, Player_var, Open_Card, Picked_Card, Drop_Card, Log = player_move_II([Player[0], Player[1]])
                
                '''
                # Code for Matching
                for c1 in list(zip(arrC, arrV)):
                    for c2 in list(zip(arrC, arrV)):
                        if c1[0] != c2[0] :
                            if pd.merge(c1[1], c2[1], on=['Rank', 'Color'], how='inner').size != 0:
                                print("Found match between ",c1[0]," and ",c2[0])
                                print(pd.merge(c1[1], c2[1], on=['Rank', 'Color'], how='inner').to_string())
                                #input("\nMatch Found...Hit enter to proceed")
                '''

                print(Player_var)
                Player_json =  [rank for rank in (Player_var.Rank.values + [color[0] for color in Player_var.Color.values])]
                Open_Card_json = [rank for rank in (Open_Card.Rank.values + [color[0] for color in Open_Card.Color.values])]
                Picked_Card_json = None
                Drop_Card_json = None
                if Picked_Card is not None:
                    Picked_Card_json = [rank for rank in (Picked_Card.Rank.values + [color[0] for color in Picked_Card.Color.values])]
                if Drop_Card is not None:
                    Drop_Card_json = [rank for rank in (Drop_Card.Rank.values + [color[0] for color in Drop_Card.Color.values])]

                Middle_Deck_Card_Count = Global_Variables.Middle_Deck_Remaining_Card_Set.shape[0]
                Open_Deck_Card_Count = Global_Variables.Open_Deck.shape[0]
                myjson = { "Player" : Player[0], 
                        "Player_Card" : Player_json,
                        "Is_Winner" : Is_Winner, 
                        "Open_Card" : Open_Card_json, 
                        "Picked_Card" : Picked_Card_json,
                        "Drop_Card" : Drop_Card_json,
                        "No_of_Rounds" : No_of_Rounds,
                        "Cards_In_Middle" : Middle_Deck_Card_Count,
                        "Cards_In_Open" : Open_Deck_Card_Count,
                        "Middle_Deck_Finish_Count" : Global_Variables.Middle_Deck_Finish_Count,
                        "Log" : Log }
                        
                await asyncio.sleep(sleep_time)
                await self.send({
                'type':'websocket.send',
                'text': json.dumps(myjson),
                })

                if Is_Winner:
                    print("Player ", Player[0]," is Winner")
                    break
                print("\n")

            if Is_Winner:
                break
            
            No_of_Rounds = No_of_Rounds + 1
            
    async def websocket_recieve(self, event):
        print("receive", event)
        

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def connect(self): 
        self.connected = True 
    
    async def disconnect(self): 
        self.connected = False
