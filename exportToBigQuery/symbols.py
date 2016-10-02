import json

inputfile = open('symbols.json', 'r')
outputfile = open('symbols.json.new', 'w')

# an input line looks like this:
# { "_id" : { "$oid" : "57f06bb27761a30b4d25252c" }, "MarketCap" : 57229811.87, "Exchange" : "NASDAQ", "IPOYear" : 0, "Symbol" : "FYT", "LastSale" : 30.935, "Name" : "First Trust Small Cap Value AlphaDEX Fund", "Industry" : "n/a", "Sector" : "n/a" }

for line in inputfile:
    x=json.loads(line)
    outputfile.write(json.dumps(x))

inputfile.close()
outputfile.close()
