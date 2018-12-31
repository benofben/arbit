import csv

with open('output.csv', 'w') as outputfile:
    writer = csv.writer(outputfile)
    output_row=['TICKER', 'DATE', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'LABEL']
    writer.writerow(output_row)

    with open('stock_prices_sample.csv') as inputfile:
        reader = csv.DictReader(inputfile)

        for row in reader:
            if float(row['HIGH'])/float(row['OPEN'])>1.02:
                label=True
            else:
                label=False

            high=float(row['HIGH'])/float(row['OPEN'])
            low=float(row['LOW'])/float(row['OPEN'])
            close=float(row['CLOSE'])/float(row['OPEN'])

            output_row=[row['TICKER'], row['DATE'], high, low, close, row['VOLUME'], label]
            writer.writerow(output_row)
