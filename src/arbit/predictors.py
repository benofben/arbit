import nasdaq.symbols.sql
import yahoo.sql
import arbit.sql
import constants

def rebuild():

	'''
	Want training points to look like:
	Outcome		High		Low			Close		Volume										TrainingDate	P(Win|(Symbol,Window))	Symbol	Exchange	IPOYear	Sector Industry	MarketCap
	{Win,Loss}	High/Open	Low/Open	Close/Open	Volume/(Sum(Volume,Window)/Size(Window))					[0,1]
	'''
	
	nasdaqSql = nasdaq.symbols.sql.sql()
	symbols = nasdaqSql.fetchSymbols()
	
	yahooSql = yahoo.sql.sql()
	
	arbitSql = arbit.sql.sql()
	arbitSql.drop_table()
	arbitSql.create_table()
	
	for symbol in symbols:
		print("Creating Training info for " + symbol)
		nasdaqInformation = nasdaqSql.fetchInformation(symbol)

		point={}		
		point['Symbol']=symbol
		point['Exchange']=nasdaqInformation['Exchange']
		point['IPOYear']=nasdaqInformation['IPOYear']
		point['Sector']=nasdaqInformation['Sector']
		point['Industry']=nasdaqInformation['Industry']
		point['MarketCap']=nasdaqInformation['MarketCap']

		yahooInformation = yahooSql.fetchInformation(symbol)
		
		if yahooInformation:
			for i in range(0, len(yahooInformation['QuoteDate'])):	
				point['Outcome']=getOutcome(i, yahooInformation)
				point['High']=yahooInformation['High'][i]/yahooInformation['Open'][i]
				point['Low']=yahooInformation['Low'][i]/yahooInformation['Open'][i]
				point['Close']=yahooInformation['Close'][i]/yahooInformation['Open'][i]
				point['Volume']=getVolume(i, yahooInformation)
				point['Date']=yahooInformation['QuoteDate'][i]
				point['PWin']=getPWin(i, yahooInformation)
				arbitSql.insert(point)
	
def getOutcome(i, yahooTrainingInformation):
	# Check if this is a training point
	if i+1<len(yahooTrainingInformation['QuoteDate']):
		if yahooTrainingInformation['High'][i+1]>yahooTrainingInformation['Open'][i+1]*(1.0+constants.take):
			outcome = 'Win'
		else:
			outcome = 'Loss'
	else:
		# test point
		outcome = 'No Data'
	return outcome
	
def getVolume(i, yahooTrainingInformation):
	avgPrice = (yahooTrainingInformation['Open'][i]+yahooTrainingInformation['Close'][i] + yahooTrainingInformation['High'][i] + yahooTrainingInformation['Low'][i])/4
	dollarVolume = yahooTrainingInformation['Volume'][i]*avgPrice
	return dollarVolume

def getVolumeAsAvg(i, yahooTrainingInformation):
	'''
	Going to compute the average volume over the last 5 days
	Then take prev/avg as our predictor 
	If we return 0, that means there wasn't enough data
	'''
	
	if i-4<0:
		return 0
	
	avgVolume = 0
	for j in range(i-4, i+1):
		avgVolume+=yahooTrainingInformation['Volume'][j]	
	avgVolume/=5
	
	# if no shares traded over the last 5 days
	if avgVolume == 0:
		return 0
	
	volume = yahooTrainingInformation['Volume'][i]/avgVolume
	return volume
	
def getPWin(i, yahooTrainingInformation):
	'''
	Going to pwin over the last 5 days
	If outcome == 'No data' for any day, then pWin=0
	'''
	
	if i-4<0:
		return 0
	
	pWin = 0
	for j in range(i-4, i+1):
		if yahooTrainingInformation['High'][j]>yahooTrainingInformation['Open'][j]*(1.0+constants.take):
			pWin+=1
		else:
			pass

	pWin/=5
	return pWin
	