import csv

with open('train.csv', 'w') as trainfile:
    train = csv.writer(trainfile)

    with open('test.csv', 'w') as testfile:
        test = csv.writer(testfile)

        output_row=['TICKER', 'DATE', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'LABEL']
        train.writerow(output_row)
        test.writerow(output_row)

        with open('stock_prices_sample.csv') as inputfile:
            reader = csv.DictReader(inputfile)

            i=0
            for row in reader:
                if float(row['HIGH'])/float(row['OPEN'])>1.02:
                    label=True
                else:
                    label=False

                open=float(row['OPEN'])
                high=float(row['HIGH'])
                low=float(row['LOW'])
                close=float(row['CLOSE'])
                volume=float(row['VOLUME'])

                n_high=round(high/open*100,2)
                n_low=round(low/open*100,2)
                n_close=round(close/open*100,2)
                n_volume=round(volume*open/1000000,2)

                output_row=[row['TICKER'], row['DATE'], n_high, n_low, n_close, n_volume, label]

                if i<800:
                    train.writerow(output_row)
                else:
                    test.writerow(output_row)
                i+=1
