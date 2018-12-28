import csv

with open('output.csv', 'w') as outputfile:
    writer = csv.writer(outputfile)
    output_row=['TICKER', 'DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'LABEL']
    writer.writerow(output_row)

    with open('stock_prices_sample.csv') as inputfile:
        reader = csv.DictReader(inputfile)

        for row in reader:
            if float(row['HIGH'])/float(row['OPEN'])>1.02:
                label=True
            else:
                label=False

            output_row=[row['TICKER'], row['DATE'], row['OPEN'], row['HIGH'], row['LOW'], row['CLOSE'], row['VOLUME'], label]
            writer.writerow(output_row)
