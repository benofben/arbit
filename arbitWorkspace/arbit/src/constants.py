import datetime

dataDirectory='I:/arbitdata/'

# used in the yahoo downloader
startDate = datetime.date.today() - datetime.timedelta(days=365)
endDate = datetime.date.today()

downloadtimeQuotes = datetime.time(0,30,0)
downloadtimeAnalysis = datetime.time(1,0,0)
downloadtimeFundamentals = datetime.time(1,30,0) #depends on the symbol files downloaded in quotes
downloadtimeEDGAR = datetime.time(2,30,0) # It looks like new master files show up at 2:01am, though are sometimes delayed as late as 2:14am.




