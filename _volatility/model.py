import csv

capital=100000.0

with open('model.csv') as inputfile:
    reader = csv.DictReader(inputfile)

    for row in reader:
        pfalse=float(row['pfalse'])
        ptrue=float(row['ptrue'])

        if ptrue>pfalse:
            # then we're going to trade

            date=row['DATE']
            open=float(row['OPEN'])
            high=float(row['HIGH'])
            close=float(row['CLOSE'])

            if high>open*1.02:
                capital=capital*1.02
            else:
                capital=capital*close/open

            print(date + ' ' + str(capital))
