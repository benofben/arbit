import quotes
import datetime

print ('Downloading...')	
quotes.downloadEverything()
print ('Done with download at ' + datetime.datetime.today().isoformat())
