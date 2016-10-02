import json

inputfile = open('../../exportData/symbols.json', 'r')
outputfile = open('../../exportData/symbols.json.new', 'w')

# an input line looks like this:
# { "_id" : { "$oid" : "57f06bb27761a30b4d25252c" }, "MarketCap" : 57229811.87, "Exchange" : "NASDAQ", "IPOYear" : 0, "Symbol" : "FYT", "LastSale" : 30.935, "Name" : "First Trust Small Cap Value AlphaDEX Fund", "Industry" : "n/a", "Sector" : "n/a" }

for line in inputfile:
    x=json.loads(line)
    x.pop("_id")
    x.pop("IPOYear")
    x.pop("Sector")
    x.pop("Industry")
    outputfile.write(json.dumps(x) + "\n")

inputfile.close()
outputfile.close()

