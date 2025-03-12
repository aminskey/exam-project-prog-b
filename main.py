from player import *
from model import Model

p = Player("Johan", 100000)
p2 = Player("Anubarbie", 100000)

m = Model()

tmpCoin = Coin("tempCoin", 500)
byteCoin = Coin("byteCoin", 1900)

p.invest(tmpCoin, 7)
p2.invest(byteCoin, 2)

tmpCoin.value += 129
byteCoin.value -= 500

p.sell(tmpCoin, 7)
p2.sell(byteCoin, 1)

p.printLog()
print(" ")
p2.printLog()

m.updatePlayerData(p)
m.updatePlayerData(p2)

m.save_to_file()
