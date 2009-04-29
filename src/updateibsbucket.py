import quotes

def update():
	symbols=['C','CS','DB','GS','RY','UBS', 'HBC', 'BAC', 'JPM', 'HBC', 'AIG', 'SHG', 'BCS', 'WFC', 'MS']

	for symbol in symbols:
		quotes.downloadQuotes(symbol)

