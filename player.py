import json
import inspect

class Coin:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.amount = 0

    def saveDict(self):
        return {
            "type": self.type,
            "value": self.value,
            "amount": self.amount
        }

    def fromDict(self, d):
        self.type = d["type"]
        self.value = d["value"]
        self.amount = d["amount"]

    def __str__(self):
        return str(self.saveDict())

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.coins = dict()
        self.history = []

    def update(self, coin):
        self.coins[coin.type] = coin.saveDict()
        if coin.amount <= 0:
            self.coins.pop(coin.type)
            self.history.append(f"Removing {coin.type.upper()} from {self.name.upper()}'s player data given that {coin.type.upper()}.amount = 0")


    def invest(self, coin: Coin, amount):
        coin.amount = amount
        self.update(coin)
        self.money -= amount * coin.value

        self.history.append(f"{self.name.upper()} invested in {coin.type.upper()}. Bought {coin.amount} unit(s) for {coin.value}")

    def sell(self, new_coin: Coin, amount):
        old_data = self.coins[new_coin.type]
        (old_coin := Coin(0, 0)).fromDict(old_data)

        self.money += amount * new_coin.value

        self.history.append(f"{self.name.upper()} sold {amount} unit(s) of {old_coin.type.upper()} for {new_coin.value}. I.e a profit of {amount * new_coin.value - amount * old_coin.value}")

        old_coin.amount -= amount
        old_coin.value = new_coin.value
        self.update(old_coin)


    def printLog(self):
        str = "  #  | Transaction history of {}".format(self.name.capitalize())
        print(str)
        for i in range(len(max(self.history)) + 7):
            print("-" if i != 5 else "+", end="")
        print(" ")

        for k, log in enumerate(self.history):
            print(f"\x1b[{(k%17)+32}m[{k:02}] | {log}\x1b[0m")


    def saveData(self):
        data = {}
        for i in inspect.getmembers(self):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    data[i[0]] = i[1]

        return data

    def __str__(self):
        return str(self.prep_data())