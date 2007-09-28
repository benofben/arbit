inputFilename = "foo2.csv"
inputFile = open(inputFilename, "rb")

import csv    
reader = csv.reader(inputFile)

outputFile = open("fooout2.csv", "w")

for time, symbol, preturn, preturn2, capital in reader:
    outputFile.write(time + "," + preturn + "," + capital + "\n")

outputFile.close()
inputFile.close()
