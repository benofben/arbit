def toMatlab(symbol):
    wekaTestToMatlab(symbol)
    wekaOutToMatlab(symbol)
    
def wekaTestToMatlab(symbol):
    wekaFile = open("data/weka/test" + symbol + ".csv")
    matlabFile = open("data/matlab/test" + symbol + ".csv", 'w')

    #toss the header line
    wekaFile.readline()
    
    for line in wekaFile:
        line=line.rstrip()
        line=line.replace("N","0")
        line=line.replace("B","1")
        matlabFile.write(line + "\n")
    wekaFile.close()
    matlabFile.close()
    
def wekaOutToMatlab(symbol):
    wekaFile = open("data/weka/" + symbol + "Out.txt")
    matlabFile = open("data/matlab/" + symbol + "Out.csv", 'w')
    for line in wekaFile:
        line=line.rstrip()
        line=line.replace(" ",",")
        line=line.replace("N","0")
        line=line.replace("B","1")
        matlabFile.write(line + "\n")
    wekaFile.close()
    matlabFile.close()
