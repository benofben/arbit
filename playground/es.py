import csv
from datetime import datetime

class es():
    orderbook = {}
    realizedpl = 0
    pl = 0
    buyprice = []

    def __init__(self):
        inputFilename='/Users/ben/Downloads/ES201606_TS.csv'
        inputFile = open(inputFilename, 'r')
        reader = csv.reader(inputFile)

        # Here's an example row:
        # 2016-02-29 00:19:35.987,193525,1,2

        for  dt, price, size, side in reader:
            if price=='Price':
                # Skip the header row
                pass
            else:
                dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f')
                price = float(price)
                size = int(size)
                side = int(side)

                if side==0:
                    self.orderbook['ask'] = price
                else:
                    self.orderbook['bid'] = price

                print(str(len(self.buyprice)) + ' ' + str(self.realizedpl)+ ' ' + str(self.pl))

        inputFile.close()

    def buy(self):
        try:
            self.buyprice.append(self.orderbook['ask'])
        except KeyError:
            pass

    def sell(self):
        try:
            self.realizedpl += self.orderbook['bid'] - self.buyprice.pop()
        except KeyError:
            pass

es()
