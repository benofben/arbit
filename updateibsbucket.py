import quotes

symbols=['C','CS','DB','GS','RY','UBS','WB', 'HBC', 'BAC', 'JPM', 'HBC', 'AIG', 'SHG', 'BCS', 'WFC', 'MS']

for symbol in symbols:
    quotes.downloadQuotes(symbol)
