import csv
import constants

def run():
    with open(constants.dataDirectory + '/symbols.csv') as f:
        symbols = f.read().splitlines()
    return symbols
