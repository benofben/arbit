import json

inputfile = open('../../exportData/fundamentals.json', 'r')
outputfile = open('../../exportData/fundamentals.json.new', 'w')

# an input line looks like this:
# { "_id" : { "$oid" : "57f076817761a30b34307199" }, "Low" : 60.19, "High" : 61.62, "Open" : 60.83, "Dividend" : 0.17, "DownloadDate" : { "$date" : "2016-10-01T18:06:03.873-0400" }, "EPS" : 1.93, "Shares" : 32290000, "InstitutionalOwnership" : 1.09, "Close" : 61.17, "Symbol" : "MNRO" }

for line in inputfile:
    x=json.loads(line)
    x.pop("_id")
    d=x.pop("DownloadDate")
    x["DownloadDate"]=d["$date"]
    outputfile.write(json.dumps(x) + "\n")

inputfile.close()
outputfile.close()

