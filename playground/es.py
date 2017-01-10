import csv
from datetime import datetime

class es():
    orderbook = {}
    capital = 0
    position = 0
    buyprice = 0

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

                if self.position==0:
                    self.buy()

                try:
                    if self.position != 0 and self.orderbook['bid']-self.buyprice > 0:
                        self.sell()
                except KeyError:
                    pass

                print(str(self.position) + ' ' + str(self.capital))

        inputFile.close()

    def buy(self):
        try:
            self.position += 1
            self.buyprice = self.orderbook['ask']
        except KeyError:
            pass

    def sell(self):
        try:
            self.position -= 1
            self.capital += self.orderbook['bid'] - self.buyprice
        except KeyError:
            pass

es()
