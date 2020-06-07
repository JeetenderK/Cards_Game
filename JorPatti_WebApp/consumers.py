import asyncio
from channels.consumer import AsyncConsumer
import csv, json
from . import Game_Logic
from .Game_Logic import *

class JorPatti_WebAppConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)

        await self.send({
            "type":"websocket.accept"
        })
            
        #obj = "Love"
        global Open_Deck
        global Middle_Deck_Remaining_Card_Set
        sleep_time = 1

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

        Middle_Deck_Remaining_Card_Set = Remaining_Card_Set
        Open_Deck = pd.DataFrame(columns=["Rank", "Color"])

        A_json = [rank for rank in (A.Rank.values + [color[0] for color in A.Color.values])]
        B_json = [rank for rank in (B.Rank.values + [color[0] for color in B.Color.values])]
        C_json = [rank for rank in (C.Rank.values + [color[0] for color in C.Color.values])]
        D_json = [rank for rank in (D.Rank.values + [color[0] for color in D.Color.values])]
        E_json = [rank for rank in (E.Rank.values + [color[0] for color in E.Color.values])]
        myjson = { "Player1" : A_json, 
                    "Player2" : B_json, 
                    "Player3" : C_json, 
                    "Player4" : D_json, 
                    "Player5" : E_json }
                        
        await asyncio.sleep(sleep_time)
        await self.send({
        'type':'websocket.send',
        'text': json.dumps(myjson),
        })

        while(1):
            A_Is_Winner, A, Open_Card, Picked_Card, Drop_Card = player_move_II(["A", A], Middle_Deck_Remaining_Card_Set, Open_Deck)
            print(A)
            A_json = [rank for rank in (A.Rank.values + [color[0] for color in A.Color.values])]
            Open_Card_json = [rank for rank in (Open_Card.Rank.values + [color[0] for color in Open_Card.Color.values])]
            Picked_Card_json = None
            Drop_Card_json = None
            if Picked_Card is not None:
                Picked_Card_json = [rank for rank in (Picked_Card.Rank.values + [color[0] for color in Picked_Card.Color.values])]
            if Drop_Card is not None:
                Drop_Card_json = [rank for rank in (Drop_Card.Rank.values + [color[0] for color in Drop_Card.Color.values])]
            myjson = { "Player1" : A_json, 
                        "Is_Winner" : A_Is_Winner, 
                        "Open_Card" : Open_Card_json, 
                        "Picked_Card" : Picked_Card_json,
                        "Drop_Card" : Drop_Card_json }
                        
            await asyncio.sleep(sleep_time)
            await self.send({
            'type':'websocket.send',
            'text': json.dumps(myjson),
            })

            if A_Is_Winner:
                print("Player A is Winner")
                break
            print("\n")
            
            
            B_Is_Winner, B, Open_Card, Picked_Card, Drop_Card = player_move_II(["B", B], Middle_Deck_Remaining_Card_Set, Open_Deck)
            print(B)
            B_json = [rank for rank in (B.Rank.values + [color[0] for color in B.Color.values])]
            Open_Card_json = [rank for rank in (Open_Card.Rank.values + [color[0] for color in Open_Card.Color.values])]
            Picked_Card_json = None
            Drop_Card_json = None
            if Picked_Card is not None:
                Picked_Card_json = [rank for rank in (Picked_Card.Rank.values + [color[0] for color in Picked_Card.Color.values])]
            if Drop_Card is not None:
                Drop_Card_json = [rank for rank in (Drop_Card.Rank.values + [color[0] for color in Drop_Card.Color.values])]
            myjson = { "Player2" : B_json, 
                        "Is_Winner" : B_Is_Winner, 
                        "Open_Card" : Open_Card_json, 
                        "Picked_Card" : Picked_Card_json,
                        "Drop_Card" : Drop_Card_json }

            await asyncio.sleep(sleep_time)
            await self.send({
            'type':'websocket.send',
            'text': json.dumps(myjson),
            })
            if B_Is_Winner:
                print("Player B is Winner")
                break
            print("\n")
            
            
            C_Is_Winner, C, Open_Card, Picked_Card, Drop_Card = player_move_II(["C", C], Middle_Deck_Remaining_Card_Set, Open_Deck)
            print(C)
            C_json = [rank for rank in (C.Rank.values + [color[0] for color in C.Color.values])]
            Open_Card_json = [rank for rank in (Open_Card.Rank.values + [color[0] for color in Open_Card.Color.values])]
            Picked_Card_json = None
            Drop_Card_json = None
            if Picked_Card is not None:
                Picked_Card_json = [rank for rank in (Picked_Card.Rank.values + [color[0] for color in Picked_Card.Color.values])]
            if Drop_Card is not None:
                Drop_Card_json = [rank for rank in (Drop_Card.Rank.values + [color[0] for color in Drop_Card.Color.values])]
            myjson = { "Player3" : C_json, 
                        "Is_Winner" : C_Is_Winner, 
                        "Open_Card" : Open_Card_json, 
                        "Picked_Card" : Picked_Card_json,
                        "Drop_Card" : Drop_Card_json }
                        
            await asyncio.sleep(sleep_time)
            await self.send({
            'type':'websocket.send',
            'text': json.dumps(myjson),
            })
            if C_Is_Winner:
                print("Player C is Winner")
                break
            print("\n")
            
            
            D_Is_Winner, D, Open_Card, Picked_Card, Drop_Card = player_move_II(["D", D], Middle_Deck_Remaining_Card_Set, Open_Deck)
            print(D)
            D_json = [rank for rank in (D.Rank.values + [color[0] for color in D.Color.values])]
            Open_Card_json = [rank for rank in (Open_Card.Rank.values + [color[0] for color in Open_Card.Color.values])]
            Picked_Card_json = None
            Drop_Card_json = None
            if Picked_Card is not None:
                Picked_Card_json = [rank for rank in (Picked_Card.Rank.values + [color[0] for color in Picked_Card.Color.values])]
            if Drop_Card is not None:
                Drop_Card_json = [rank for rank in (Drop_Card.Rank.values + [color[0] for color in Drop_Card.Color.values])]
            myjson = { "Player4" : D_json, 
                        "Is_Winner" : D_Is_Winner, 
                        "Open_Card" : Open_Card_json, 
                        "Picked_Card" : Picked_Card_json,
                        "Drop_Card" : Drop_Card_json }
                        
            await asyncio.sleep(sleep_time)
            await self.send({
            'type':'websocket.send',
            'text': json.dumps(myjson),
            })
            if D_Is_Winner:
                print("Player D is Winner")
                break
            print("\n")
            
            
            E_Is_Winner, E, Open_Card, Picked_Card, Drop_Card = player_move_II(["E", E], Middle_Deck_Remaining_Card_Set, Open_Deck)
            print(E)
            E_json = [rank for rank in (E.Rank.values + [color[0] for color in E.Color.values])]
            Open_Card_json = [rank for rank in (Open_Card.Rank.values + [color[0] for color in Open_Card.Color.values])]
            Picked_Card_json = None
            Drop_Card_json = None
            if Picked_Card is not None:
                Picked_Card_json = [rank for rank in (Picked_Card.Rank.values + [color[0] for color in Picked_Card.Color.values])]
            if Drop_Card is not None:
                Drop_Card_json = [rank for rank in (Drop_Card.Rank.values + [color[0] for color in Drop_Card.Color.values])]
            myjson = { "Player5" : E_json, 
                        "Is_Winner" : E_Is_Winner, 
                        "Open_Card" : Open_Card_json, 
                        "Picked_Card" : Picked_Card_json,
                        "Drop_Card" : Drop_Card_json }
                        
            await asyncio.sleep(sleep_time)
            await self.send({
            'type':'websocket.send',
            'text': json.dumps(myjson),
            })

            if E_Is_Winner:
                print("Player E is Winner")
                break
            print("\n")
               
            
    async def websocket_recieve(self, event):
        print("receive", event)
        

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def connect(self): 
        self.connected = True 
    
    async def disconnect(self): 
        self.connected = False