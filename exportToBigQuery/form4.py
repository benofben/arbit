import json

inputfile = open('../../exportData/form4.json', 'r')
outputfile = open('../../exportData/form4.json.new', 'w')

# an input line looks like this:
# { "_id" : { "$oid" : "57ef2009b16f58544bd98063" }, "IsTenPercentOwner" : "F", "TransactionShares" : 200, "IsDirector" : "T", "IsOther" : "F", "RptOwnerCik" : "0001206513", "AcceptanceDatetime" : { "$date" : "2016-09-30T13:38:58.000-0400" }, "SecDocument" : "0001140361-16-081269.txt : 20160930 4", "TransactionPricePerShare" : 152.27, "RptOwnerName" : "ROPER MARTIN F", "IsOfficer" : "T", "TransactionAcquiredDisposed" : "D", "IssuerTradingSymbol" : "SAM", "SharesOwned" : 32273, "TransactionDate" : { "$date" : "2016-09-28T20:00:00.000-0400" } }

for line in inputfile:
    x=json.loads(line)
    x.pop("_id")

    d=x.pop("AcceptanceDatetime")
    x["Date"]=d["$date"]

    d=x.pop("TransactionDate")
    x["Date"]=d["$date"]

    outputfile.write(json.dumps(x) + "\n")

inputfile.close()
outputfile.close()

