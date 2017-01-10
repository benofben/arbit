import csv
import datetime

inputFilename='/Users/ben/Downloads/ES201606_TS.csv'
inputFile = open(inputFilename, 'r')

reader = csv.reader(inputFile)

for  datetime, price, size, side in reader:
    if price=='Price':
        # Skip the header row
        pass
    else:
        datetime = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
        price = float(price)
        size = int(size)
        side = int(side)

    print(datetime)
inputFile.close()
