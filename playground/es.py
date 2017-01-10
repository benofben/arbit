import csv
from datetime import datetime

inputFilename='/Users/ben/Downloads/ES201606_TS.csv'
inputFile = open(inputFilename, 'r')
reader = csv.reader(inputFile)

# Here's an example row:
# 2016-02-29 00:19:35.987,193525,1,2

orderbook = {}

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
            orderbook['ask'] = price
        else:
            orderbook['bid'] = price

inputFile.close()
