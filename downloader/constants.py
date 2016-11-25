import datetime

dataDirectory='/home/benton_lackey/arbit_data/'

# these seem to be updated as they come out
# We're going to end up lagging a day for this
downloadtimeAnalysis = datetime.time(0,0,0)

# not sure when these update, but they don't change often
# want to refresh them before quotes
downloadtimeSymbols = datetime.time(0,10,0)

# new quotes don't show up until after 12am
downloadtimeQuotes = datetime.time(0,30,0)

# depends on the symbols download
# run right after market close
downloadtimeFundamentals = datetime.time(16,30,0)

# It looks like new master files show up at 2:01am, though are sometimes delayed as late as 2:14am.
# Something else is showing up at 10pm eastern, but it's unclear from my old comments.  Need to investigate.
downloadtimeEDGAR = datetime.time(22,30,0)
