'''
import symbols
symbols.downloadSymbols()

import quotes
quotes.downloadAllQuotes()
'''

### now we're going to go through and delete some stocks we don't like
import data
symbols=data.getSymbols()
quotes=data.getAllQuotes()

# this violates any sane sort of validation...
import os
for symbol in quotes:
    if quotes[symbol]['Volume'][-1]<1000000:
            filename='data/quotes/' + symbol + '.csv'
            if os.path.exists(filename):
                os.remove(filename)
                print 'Deleted ' + symbol + '.'
            else:
                print 'Failed to delete ' + symbol + '.'
        
