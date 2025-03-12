import json
import requests

from player import Player, Coin

class Model:
    """
        [12/03/25: DONE] Add self.playerDict
        [12/03/25: DONE] Make a function that will update self.playerDict
        [12/03/25: DONE] Make a function that will save self.playerDict in a file
        [12/03/25] Make a function that will load playerdata.json into self.__playerDict
    """
    def __init__(self):
        self.__playerDict = {}


    def updatePlayerData(self, p):
        self.__playerDict[p.name] = p.saveData()


    def load_from_file(self):
        with open("playerdata.json", "r") as f:
            tmp = json.load(f)
            f.close()
        
        for player in tmp.items():
            p = Player(tmp[player].name, tmp[player].money)
            p.history = tmp[player].history

            for coin in tmp["coins"]:
                c = Coin("", 0)
                c.type = tmp[player][coin]["type"]
                # TODO: Finish function...


    def save_to_file(self):
        with open("playerdata.json", "w") as f:
            f.write(json.dumps(self.__playerDict, indent=4))
            f.close()

    def get_data(self, curr="dkk"):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        parameters = {
            "vs_currency": curr, 
            "sparkline": "true"
        }

        response = requests.get(url, params=parameters)
        if response.status_code == 200:
            data = response.json()
            return data
        print(f"Error: {response.status_code}")

    # TODO: [11-03-25] Implement a method to load playerdata for all players and create Player objects
    # TODO: [11-03-25] Implement a method to save playerdata for all the players
    # TODO: [11-03-25] Add self.controller