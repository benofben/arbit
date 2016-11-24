import datetime

dataDirectory='/home/benton_lackey/arbit_data/'

# used in the yahoo downloader
startDate = datetime.date.today() - datetime.timedelta(days=365)
endDate = datetime.date.today()

# these seem to be updates as they come out.  Run after midnight.
# We're going to end up lagging a day for this.
downloadtimeAnalysis = datetime.time(0,0,1)

# new quotes don't show up until after 12am.
downloadtimeQuotes = datetime.time(0,30,0)

# depends on the symbol files downloaded in quotes
# could probably run right after market close
# going to also pull down ohlc.  This will give us data a couple hours earlier than yahoo.
downloadtimeFundamentals = datetime.time(16,30,0)

# It looks like new master files show up at 2:01am, though are sometimes delayed as late as 2:14am.
# It's now unclear what timezone this is.  It might be gmt, in which case the files show up a little after 9.
# the mail job that is part of this needs fundamentals (which now includes scraped quotes) to finish first.

# ... showing up at 10pm eastern.
downloadtimeEDGAR = datetime.time(22,30,0)
