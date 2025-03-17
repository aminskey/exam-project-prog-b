import json
import requests

from player import Player, Coin

class Model:
    """
        Tasks
        [12/03/25: DONE] Add self.playerDict
        [12/03/25: DONE] Make a function that will update self.playerDict
        [12/03/25: DONE] Make a function that will save self.playerDict in a file
        [12/03/25] Make a function that will load playerdata.json into self.__playerDict
        Added changes:
        [13/03/25 from working-on-views] Making __playerDict read-only (to be used in views later on...)
    """
    def __init__(self):
        self.playerData = {}
        self.players = {}
        self.controller = None


    @property
    def playerDict(self):
        return self.__playerDict

    def updatePlayerData(self, p):
        self.playerData[p.name] = p.saveData()


    def load_from_file(self):
        with open("playerdata.json", "r") as f:
            tmp = json.load(f)
            f.close()        


        for player, data in tmp.items():
            p = Player(data["name"], data["money"])
            p.history = data["history"]

            for coin, cdata in data["coins"].items():
                print(coin, cdata)
                c = Coin(str(coin), cdata["value"])
                c.amount = cdata["amount"]
                p.update(c)
            
            self.players[p.name] = p
                


    def save_to_file(self):
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
        return dict(error="Couldn't get data :( Code: {}".format(response.status_code))

    # TODO: [11-03-25] Implement a method to load playerdata for all players and create Player objects
    # TODO: [11-03-25] Implement a method to save playerdata for all the players
    # TODO: [11-03-25] Add self.controller