from datastructures import Queue

class Coin:
    def __init__(self, type, value, meta=None):
        self.type = type
        self.value = value
        self.amount = 0

        # We don't want to save this
        self.meta = meta


    def saveDict(self):
        return {
            "type": self.type,
            "value": self.value,
            "amount": self.amount
        }

    # Loading values from dictionary (Mainly the one in playerdata.json)
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


    def getAmountOfCoin(self, type):
        if type not in self.coins:
            return 0

        q = self.coins[type]
        amounts = q.seekAllByAttr("amount")
        k = 0
        for i in amounts:
            k += i.amount

        return k

    def invest(self, coin: Coin, amount):
        if coin.type not in self.coins:
            self.coins[coin.type] = Queue()
        q = self.coins[coin.type]

        self.money -= amount * coin.value

        coin.amount = amount

        ret = q.seekByAttrVal("value", coin.value)
        if not ret:
            print("no return...")
            "coin.amount = amount"
            q.push(coin)
        else:
            print("return true")
            i, _ = ret
            q.arr[i].amount += coin.amount

        self.history.append(f"{self.name.upper()} bought {amount} unit(s) of {coin.type} for a price of {coin.value} pr. coin.")

    def sell(self, coin: Coin, amount):
        if not coin.type in self.coins:
            print("Coin type not in self.coins")
            return

        firstCoin = self.coins[coin.type].arr[0]
        newAmount = firstCoin.amount - amount

        if newAmount <= 0:
            self.coins[coin.type].pop()
            self.money += firstCoin.amount * coin.value
            finalAmount = firstCoin.amount
        else:
            self.money += amount * coin.value
            firstCoin.amount -= amount
            finalAmount = amount

        self.history.append(
            f"{self.name.upper()} sold {finalAmount} unit(s) of {firstCoin.type.upper()} for {coin.value}. I.e a profit of {amount * coin.value - amount * firstCoin.value}")


    def printLog(self):
        str = "  #  | Transaction history of {}".format(self.name.capitalize())
        print(str)
        for i in range(len(max(self.history)) + 7):
            print("-" if i != 5 else "+", end="")
        print(" ")

        for k, log in enumerate(self.history):
            print(f"\x1b[{(k%17)+32}m[{k:02}] | {log}\x1b[0m")

    def genJSON(self):
        data = {
            "name": self.name,
            "money": self.money,
            "history": self.history,
            "coins": dict()
        }

        for coin in self.coins:
            q = self.coins[coin]
            a = []

            for i in q.arr:
                a.append(i.saveDict())

            data["coins"][coin] = a

        """
        for i in inspect.getmembers(self):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    data[i[0]] = i[1]
        """

        return data

    def __str__(self):
        return str(self.genJSON())