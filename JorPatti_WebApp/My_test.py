import pandas as pd
import os
import random
import numpy as np


def main():
    
    Players = ['A','B','C','D','E']
    Number_of_Cards_per_player = 5
    Remaining_Card_Set = pd.read_csv(os.path.abspath(os.getcwd() + '/../Cards.csv'), index_col="Index")
    List_of_Player_with_Cards = {}

    for Player in Players:
        abc = Remaining_Card_Set.sample(n = Number_of_Cards_per_player, random_state = random.randint(0,100))
        Remaining_Card_Set = Remaining_Card_Set.drop(abc.index.values)
        temp = [card[0] + card[1][0] + ".png" for card in abc.values.tolist()]
        List_of_Player_with_Cards.update({Player: temp})

    return List_of_Player_with_Cards
    
    #c = {"cards":["AC.png","AD.png","AH.png","AS.png"]}