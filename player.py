import json

from inspect import getmembers

class Player:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.coins = kwargs["coins"]
        self.data = {
            "name": self.name,
            "coins": self.coins
        }



    def load_from_file(self, file):
        with open(file, "r") as f:
            self.data = json.load(f)
            f.close()

    def save_to_file(self, out):
        with open(out, "w") as f:
            f.write(json.dumps(self.data, indent=4))
            f.close()