import quotes

def update():
	symbols=['C','CS','DB','GS','RY','UBS', 'HBC', 'BAC', 'JPM', 'HBC', 'AIG', 'SHG', 'BCS', 'WFC', 'MS']
	
	'''
	symbols=[
		'AIB',
		'AIG',
		'BAC',
		'BCS',
		'C',
		'CS',
		'DB',
		'GS',
		'HBC',
		'JPM',
		'LYG'
		'MS',
		'NMR',
		'PNC',
		'RBS',
		'RY',
		'SHG',
		'STI',
		'UBS',
		'USB',
		'WFC'
	]
	'''
	
	
	quotes.cleanUp()
	for symbol in symbols:		
		quotes.downloadQuotes(symbol)

