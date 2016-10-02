import json

inputfile = open('../../exportData/fundamentals.json', 'r')
outputfile = open('../../exportData/fundamentals.json.new', 'w')

# an input line looks like this:
# { "_id" : { "$oid" : "57f076817761a30b34307199" }, "Low" : 60.19, "High" : 61.62, "Open" : 60.83, "Dividend" : 0.17, "DownloadDate" : { "$date" : "2016-10-01T18:06:03.873-0400" }, "EPS" : 1.93, "Shares" : 32290000, "InstitutionalOwnership" : 1.09, "Close" : 61.17, "Symbol" : "MNRO" }

# BigQuery doesn't like the Mongo date format:
# JSON parsing error in row starting at position 0 at file: gs://mongoexport/form4.json.new. Could not parse '2014-04-02T20:00:00.000-0400' as a timestamp. Required format is YYYY-MM-DD HH:MM[:SS[.SSSSSS]] Field: Date; Value: 2014-04-02T20:00:00.000-0400 (error code: invalid)

for line in inputfile:
    x=json.loads(line)
    x.pop("_id")
    d=x.pop("DownloadDate")
    x["DownloadDate"]=d["$date"]
    outputfile.write(json.dumps(x) + "\n")

inputfile.close()
outputfile.close()

