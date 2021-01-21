import csv
import constants
import pandas


def run():
    quotes = pandas.read_csv (constants.dataDirectory + '/quotes.csv')
    print(quotes)
    return(quotes)

run()
