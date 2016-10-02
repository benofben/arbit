import json

inputfile = open('../../exportData/ratingsChanges.json', 'r')
outputfile = open('../../exportData/ratingsChanges.json.new', 'w')

# an input line looks like this:
# { "_id" : { "$oid" : "56987cdab16f580a9da854cc" }, "Ticker" : "AMC", "BrokerageFirm" : "MKM Partners", "Company" : "AMC Entertainment", "RatingsChangeType" : "Downgrade", "RatingsChangeDate" : { "$date" : "2015-04-08T20:00:00.000-0400" }, "PriceTarget" : "$35 to $37", "RatingsChange" : "Buy to Neutral" }

for line in inputfile:
    x=json.loads(line)
    x.pop("_id")
    d=x.pop("RatingsChangeDate")
    x["RatingsChangeDate"]=d["$date"]
    outputfile.write(json.dumps(x) + "\n")

inputfile.close()
outputfile.close()

