from player import *

p = Player("Johan", 100000)
tmpCoin = Coin("tempCoin", 500)
byteCoin = Coin("byteCoin", 1900)

p.invest(tmpCoin, 7)
p.invest(byteCoin, 2)

tmpCoin.value += 129
byteCoin.value -= 500

p.sell(tmpCoin, 7)
p.sell(byteCoin, 1)

p.printLog()

p.save_to_file()