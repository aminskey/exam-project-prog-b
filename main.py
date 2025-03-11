from player import *

p = Player("Johan", 100000)
tmpCoin = Coin("tempCoin", 500)

p.invest(tmpCoin, 7)

tmpCoin.value += 129

p.sell(tmpCoin, 7)

p.printLog()

p.save_to_file()