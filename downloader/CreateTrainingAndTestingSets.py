import os
def CreateTrainingAndTestingSetsForSymbol(symbol):
    inputFilename = "data/reformattedQuotes/" + symbol + ".csv"
    inputFile = open(inputFilename, "rb")
    lines=[]
    for line in inputFile:
        lines.append(line)
    inputFile.close()

    if not os.path.exists("data/train"):
        os.makedirs("data/train")
    if not os.path.exists("data/test"):
        os.makedirs("data/test")
    
    trainFilename = "data/train/" + symbol + ".csv"
    trainFile = open(trainFilename, 'w')
    for line in lines[0:int(len(lines)/2)]:
        trainFile.write(line)
    trainFile.close()
    testFilename = "data/test/" + symbol + ".csv"
    testFile = open(testFilename, 'w')
    for line in lines[int(len(lines)/2+1):]:
        testFile.write(line)
    testFile.close()

import ReformatQuotes
def CreateTrainingAndTestingSets():
    symbols=ReformatQuotes.GetSymbols('data/reformattedQuotes')
    while symbols:
        symbol = symbols.pop()
        print "Processing symbol " + symbol + "."
        print str(len(symbols)) + " symbols remaining.\n"
        CreateTrainingAndTestingSetsForSymbol(symbol)
