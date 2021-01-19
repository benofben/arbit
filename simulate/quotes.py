import csv
import constants
import pandas

def run():
    quotes=[]
    with open(constants.dataDirectory + '/quotes.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quotes.append(row)

    return(quotes)

run()
