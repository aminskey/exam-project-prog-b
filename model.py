import json
import requests

class Model:
    """
        - Add self.playerDict
        - Make a function that will update self.playerDict
        - Make a function that will save self.playerDict in a file
    """
    def __init__(self):
        self.__playerDict = {}

    def updatePlayerData(self, p):
        self.__playerDict[p.name] = p.saveData()


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

    # TODO: Implement a method to load playerdata for all players and create Player objects
    # TODO: Implement a method to save playerdata for all the players
    # TODO: Add self.controller