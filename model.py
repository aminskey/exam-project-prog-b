import json
import requests

from player import Player, Coin
from datastructures import Queue

class Model:
    """
        List of tasks:

        [12/03/25: DONE] Add self.playerDict
        [12/03/25: DONE] Make a function that will update self.playerDict
        [12/03/25: DONE] Make a function that will save self.playerDict in a file
        [12/03/25-17/03/25: DONE] Make a function that will load playerdata.json into self.__playerDict
        [24/03/25-25/03/25: DONE] Make a function that will load all coins into corresponding coin objects
    """
    def __init__(self):
        self.playerData = {}
        self.players = {}
        self.__coins = {}
        self.controller = None
        self.codes = None

    def get_err_codes(self):
        with open("codes.json", "r") as f:
            self.codes = json.load(f)
            f.close()

    def get_coins(self):
        return self.__coins

    def updatePlayerData(self):
        for name, p in self.players.items():
            self.playerData[name] = p.genJSON()

    def savePlayer(self, p):
        self.playerData[p.name] = p.genJSON()


    def load_from_file(self, file):
        with open(file, "r") as f:
            tmp = json.load(f)
            f.close()        


        for player, data in tmp.items():
            p = Player(data["name"], data["money"])
            p.history = data["history"]


            for key, cdata in data["coins"].items():
                q = Queue()
                for coin in cdata:
                    c = Coin(coin["name"], coin["value"])
                    c.amount = coin["amount"]
                    q.push(c)
                p.coins[key] = q


                # TODO: Make a queue with updated coin information
            
            self.players[p.name] = p
                


    def save_to_file(self):
        self.updatePlayerData()
        with open("playerdata.json", "w") as f:
            f.write(json.dumps(self.playerData, indent=4))
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

        self.get_err_codes()
        st_code = self.codes[f"{response.status_code}"]

        return dict(error=f"{response.status_code}: {st_code['message']}", msg=f"{st_code['description']}")

    # Parsing data from coingecko, and creating corresponding coin objects.
    def load_coins(self, data):
        for coin_data in data:
            coin = Coin(
                type=coin_data["name"],
                value=coin_data["current_price"],
                meta=coin_data
            )
            self.__coins[coin.type] = coin

    # TODO: [11-03-25] Implement a method to load playerdata for all players and create Player objects
    # TODO: [11-03-25] Implement a method to save playerdata for all the players
    # TODO: [11-03-25] Add self.controller