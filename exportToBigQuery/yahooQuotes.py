import json

inputfile = open('../../exportData/yahooQuotes.json', 'r')
outputfile = open('../../exportData/yahooQuotes.json.new', 'w')

# an input line looks like this:
# { "_id" : { "$oid" : "57f089467761a30b4dfc0eb1" }, "AdjustedClose" : 23.99984, "Close" : 24.459999, "High" : 24.99, "Symbol" : "LHO", "Low" : 24.42, "Volume" : 1222900, "Date" : { "$date" : "2016-09-18T20:00:00.000-0400" }, "Open" : 24.83 }

for line in inputfile:
    x=json.loads(line)
    x.pop("_id")
    d=x.pop("Date")
    x["Date"]=d["$date"]
    outputfile.write(json.dumps(x) + "\n")

inputfile.close()
outputfile.close()
