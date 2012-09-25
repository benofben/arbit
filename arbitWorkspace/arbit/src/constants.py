import datetime

dataDirectory='I:/arbitdata/'

# used in the yahoo downloader
startDate = datetime.date.today() - datetime.timedelta(days=365)
endDate = datetime.date.today()

# these seem to be updates as they come out.  Run after midnight.  
# We're going to end up lagging a day for this.
downloadtimeAnalysis = datetime.time(0,0,1)

# download right after market close
downloadtimeQuotes = datetime.time(16,30,0)

#depends on the symbol files downloaded in quotes
# could probably run right after market close
downloadtimeFundamentals = datetime.time(16,30,0) 

# It looks like new master files show up at 2:01am, though are sometimes delayed as late as 2:14am.
# It's now unclear what timezone this is.  It might be gmt, in which case the files show up a little after 9.
downloadtimeEDGAR = datetime.time(21,30,0) 




