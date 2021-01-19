import json

def convertDate(olddate):
    # BigQuery doesn't like the Mongo date format:
    # JSON parsing error in row starting at position 0 at file: gs://mongoexport/form4.json.new.
    # Could not parse '2014-04-02T20:00:00.000-0400' as a timestamp.
    # Required format is YYYY-MM-DD HH:MM[:SS[.SSSSSS]] Field: Date; Value: 2014-04-02T20:00:00.000-0400
    # (error code: invalid)

    try:
        newdate = olddate.replace("T", " ")
    except AttributeError:
        print("Got an attribute error while parsing date: " + str(olddate))
        exit(1)
    return newdate

def convertBoolean(b):
    if b=='T' or b =='A':
        return True
    elif b=='F' or b=='D':
        return False
    else:
        print("Parse error for boolean value: " + b)
        exit(1)

def yahooQuotes():
    filename = '../../exportData/yahooQuotes.json'
    inputfile = open(filename, 'r')
    outputfile = open(filename+'.bigquery', 'w')

    # an input line looks like this:
    # { "_id" : { "$oid" : "57f089467761a30b4dfc0eb1" }, "AdjustedClose" : 23.99984, "Close" : 24.459999, "High" : 24.99, "Symbol" : "LHO", "Low" : 24.42, "Volume" : 1222900, "Date" : { "$date" : "2016-09-18T20:00:00.000-0400" }, "Open" : 24.83 }

    for line in inputfile:
        x = json.loads(line)
        x.pop("_id")
        d = x.pop("Date")
        x["Date"] = convertDate(d["$date"])
        outputfile.write(json.dumps(x) + "\n")

    inputfile.close()
    outputfile.close()


def symbols():
    filename = '../../exportData/symbols.json'
    inputfile = open(filename, 'r')
    outputfile = open(filename+'.bigquery', 'w')

    # an input line looks like this:
    # { "_id" : { "$oid" : "57f06bb27761a30b4d25252c" }, "MarketCap" : 57229811.87, "Exchange" : "NASDAQ", "IPOYear" : 0, "Symbol" : "FYT", "LastSale" : 30.935, "Name" : "First Trust Small Cap Value AlphaDEX Fund", "Industry" : "n/a", "Sector" : "n/a" }

    for line in inputfile:
        x = json.loads(line)
        x.pop("_id")
        x.pop("IPOYear")
        x.pop("Sector")
        x.pop("Industry")
        outputfile.write(json.dumps(x) + "\n")

    inputfile.close()
    outputfile.close()


def ratingsChanges():
    filename = '../../exportData/ratingsChanges.json'
    inputfile = open(filename, 'r')
    outputfile = open(filename+'.bigquery', 'w')

    # an input line looks like this:
    # { "_id" : { "$oid" : "56987cdab16f580a9da854cc" }, "Ticker" : "AMC", "BrokerageFirm" : "MKM Partners", "Company" : "AMC Entertainment", "RatingsChangeType" : "Downgrade", "RatingsChangeDate" : { "$date" : "2015-04-08T20:00:00.000-0400" }, "PriceTarget" : "$35 to $37", "RatingsChange" : "Buy to Neutral" }

    for line in inputfile:
        x = json.loads(line)
        x.pop("_id")
        d = x.pop("RatingsChangeDate")
        x["RatingsChangeDate"] = convertDate(d["$date"])
        outputfile.write(json.dumps(x) + "\n")

    inputfile.close()
    outputfile.close()


def fundamentals():
    filename = '../../exportData/fundamentals.json'
    inputfile = open(filename, 'r')
    outputfile = open(filename+'.bigquery', 'w')

    # an input line looks like this:
    # { "_id" : { "$oid" : "57f076817761a30b34307199" }, "Low" : 60.19, "High" : 61.62, "Open" : 60.83, "Dividend" : 0.17, "DownloadDate" : { "$date" : "2016-10-01T18:06:03.873-0400" }, "EPS" : 1.93, "Shares" : 32290000, "InstitutionalOwnership" : 1.09, "Close" : 61.17, "Symbol" : "MNRO" }

    for line in inputfile:
        x = json.loads(line)
        x.pop("_id")
        d = x.pop("DownloadDate")
        x["DownloadDate"] = convertDate(d["$date"])
        outputfile.write(json.dumps(x) + "\n")

    inputfile.close()
    outputfile.close()

def form4():
    filename = '../../exportData/form4.json'
    inputfile = open(filename, 'r')
    outputfile = open(filename+'.bigquery', 'w')

    # an input line looks like this:
    # { "_id" : { "$oid" : "57ef2009b16f58544bd98063" }, "IsTenPercentOwner" : "F", "TransactionShares" : 200, "IsDirector" : "T", "IsOther" : "F", "RptOwnerCik" : "0001206513", "AcceptanceDatetime" : { "$date" : "2016-09-30T13:38:58.000-0400" }, "SecDocument" : "0001140361-16-081269.txt : 20160930 4", "TransactionPricePerShare" : 152.27, "RptOwnerName" : "ROPER MARTIN F", "IsOfficer" : "T", "TransactionAcquiredDisposed" : "D", "IssuerTradingSymbol" : "SAM", "SharesOwned" : 32273, "TransactionDate" : { "$date" : "2016-09-28T20:00:00.000-0400" } }

    for line in inputfile:
        x = json.loads(line)
        x.pop("_id")

        d = x.pop("AcceptanceDatetime")
        x["AcceptanceDatetime"] = convertDate(d["$date"])

        d = x.pop("TransactionDate")
        x["TransactionDate"] = convertDate(d["$date"])

        d = x.pop("IsDirector")
        x["IsDirector"] = convertBoolean(d)

        d = x.pop("IsOther")
        x["IsOther"] = convertBoolean(d)

        d = x.pop("IsOfficer")
        x["IsOfficer"] = convertBoolean(d)

        d = x.pop("IsTenPercentOwner")
        x["IsTenPercentOwner"] = convertBoolean(d)

        d = x.pop("TransactionAcquiredDisposed")
        x["TransactionAcquired"] = convertBoolean(d)

        outputfile.write(json.dumps(x) + "\n")

    inputfile.close()
    outputfile.close()

def run():
# It looks like the mongo export for form4 has a bunch of garbage data.  Going to try using the raw data instead
#    form4()

    yahooQuotes()
    symbols()
    ratingsChanges()
    fundamentals()

run()