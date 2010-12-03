#import sys	# for maxint
import constants
import yahoo.quotes as quotesYahoo
import yahoo.predictors as predictors
import datetime
import multiprocessing


def run(currentDate, quotes, symbolInformation):
	[trainingSet, testSet]=createDataSet(currentDate, quotes, symbolInformation)
	pWin=computeP(trainingSet, testSet)
	
	sortedSymbols = sorted(pWin, key=pWin.__getitem__, reverse=True)
	bestSymbols = sortedSymbols[0:3]
	
	return bestSymbols
		
def createDataSet(currentDate, quotes, symbolInformation):
	symbols = findQualifyingSymbols(currentDate, quotes, symbolInformation)
	
	trainingSet = []
	# going to create a training set for some window back in time starting with currentDate-1
	date = currentDate - datetime.timedelta(days=100)
	while date<currentDate:
		trainingSet = trainingSet + createTrainingSetForDate(date, symbols, quotes, symbolInformation)
		date = date + datetime.timedelta(days=1)
	# the test set should include data up to and including currentDate
	testSet = createTestSetForDate(date, symbols, quotes, symbolInformation)
	
	return [trainingSet, testSet]

def findQualifyingSymbols(currentDate, quotes, symbolInformation):
	# Create a list of symbols that meet requirements for training.
	# Volume for currentDate - 1 > 10^6
	# Market cap > 10^9
	# Has currentDate - 50 days of market data
	symbols = []
	for symbol in symbolInformation:
		if symbol in quotes:
			volume = quotes[symbol]['Volume'][quotesYahoo.getIndex(currentDate, quotes[symbol])]
			enoughData = quotesYahoo.getSubquoteForSymbolWithWindow(symbol, currentDate, quotes, 100)
			
			if symbolInformation[symbol]['MarketCap']>10**9 and volume > 10**6 and enoughData:
				symbols.append(symbol)
	return symbols
		
# this function is mostly duplicated in quotesYahoo
def getMostRecentTradingDayForSymbolBeforeCurrentDate(symbol, currentDate, quotes):
	# in the case that a symbol was delisted some time ago, this will still suggest that symbol -- need to fix this
	index = quotesYahoo.getIndex(currentDate, quotes[symbol])
	if index:
		return quotes[symbol]['Date'][index-1]
	return quotes[symbol]['Date'][-1]
		
def createTrainingSetForDate(date, symbols, quotes, symbolInformation):
	trainingSet = []
	for symbol in symbols:
		trainingSet.append(createTrainingPointForDateForSymbol(date, symbol, quotes, symbolInformation))
	return trainingSet

def createTestSetForDate(date, symbols, quotes, symbolInformation):
	testSet = []
	for symbol in symbols:
		testSet.append(createTestPointForDateForSymbol(date, symbol, quotes, symbolInformation))
	return testSet
	
def createTrainingPointForDateForSymbol(date, symbol, quotes, symbolInformation):
	#This is the same as a test set, but with an Outcome entry in the dictionary as well
	trainingPoint = createTestPointForDateForSymbol(date, symbol, quotes, symbolInformation)
	
	trainingPointDateIndex = quotesYahoo.getIndex(date, quotes[symbol])
	Open = quotes[symbol]['Open'][trainingPointDateIndex+1]
	High = quotes[symbol]['High'][trainingPointDateIndex+1]
	if(High>Open*(1.0+constants.take)):
		trainingPoint['Outcome']='Win'
	else:
		trainingPoint['Outcome']='Loss'
	return trainingPoint
	
def createTestPointForDateForSymbol(date, symbol, quotes, symbolInformation):
	# We want to build sets of the form:
	# testSet[i][Exchange, Symbol, MarketCap, IPOyear, Sector, Industry, pWin(t={1,5,10}), Volume(t=1)]
	testPoint={}
	testPoint['Exchange']=symbolInformation[symbol]['Exchange']
	testPoint['Symbol']=symbol
		
	testPoint['MarketCap']=symbolInformation[symbol]['MarketCap']
	testPoint['MarketCap']=roundToTheNearestBillion(testPoint['MarketCap'])
		
	testPoint['IPOYear']=symbolInformation[symbol]['IPOYear']
	testPoint['Sector']=symbolInformation[symbol]['Sector']
	testPoint['Industry']=symbolInformation[symbol]['Industry']
	
	# Not particularly independent
	#testPoint['Volume']=roundToTheNearestMillion(quotes[symbol]['Volume'][quotesYahoo.getIndex(date, quotes[symbol])])
	
	for i in (1,5,8): #(1,2,3,5,8,13,21,34,55, 89, 144):
		testPoint['pWin' + str(i)]=bin(predictors.pWin(date, symbol, quotes, i))
	
	return testPoint
		
def computeP(trainingSet, testSet):
	args = []
	for testPoint in testSet:
		args.append([trainingSet, testPoint])
	
	pool = multiprocessing.Pool(multiprocessing.cpu_count())
	p=pool.map(classify, args)
	
	pWin = {}
	i=0
	for result in p:
		pWin[testSet[i]['Symbol']] = result['Win']
		i=i+1

	return pWin
	
def classify(args):
	[trainingSet, testPoint] = args
	if not trainingSet or len(trainingSet)==0:
		return False
	
	classes=['Win', 'Loss']
	
	# compute p(C)
	p_C={}
	for C in classes:
		p_C[C]=0.0
		for i in range(0, len(trainingSet)):
			if trainingSet[i]['Outcome']==C:
				p_C[C]+=1
		p_C[C]/=len(trainingSet)
			
	# compute p(F_i|C)
	p_F_C={}
	c_F_C={}
	for predictor in testPoint:
		if predictor!='Outcome':
			p_F_C[predictor]={}
			c_F_C[predictor]={}
			for C in classes:
				p_F_C[predictor][C]=0.0
				c_F_C[predictor][C]=0
		
	for i in range(0, len(trainingSet)):
		for predictor in trainingSet[i]:
			if predictor!='Outcome':
				C=trainingSet[i]['Outcome']
				if trainingSet[i][predictor]==testPoint[predictor]:
					p_F_C[predictor][C]+=1
				c_F_C[predictor][C]+=1
		
	for predictor in p_F_C:
		for C in p_F_C[predictor]:
			if c_F_C[predictor][C]==0:
				p_F_C[predictor][C]=0
			else:
				p_F_C[predictor][C]/=c_F_C[predictor][C]
		
	# compute p(F_i)
	p_F={}
	c_F={}
	for predictor in testPoint:
		if predictor!='Outcome':
			p_F[predictor]=0.0
			c_F[predictor]=0
		
	for i in range(0, len(trainingSet)):
		for predictor in trainingSet[i]:
			if predictor!='Outcome':
				if trainingSet[i][predictor]==testPoint[predictor]:
					p_F[predictor]+=1
				c_F[predictor]+=1
	for predictor in p_F:
		p_F[predictor]/=c_F[predictor]
		
	#compute p(C) * pi[p(F_i|C)/p(F_i)]
	p={}
	for C in classes:
		p[C]=p_C[C]
		for predictor in p_F:
			if p_F[predictor]!=0:
				p[C]*=p_F_C[predictor][C]/p_F[predictor]
	
	# scale p(C) by 1/Z
	Z=0
	for C in p:
		Z=Z+p[C]
	for C in p:
		p[C]=p[C]/Z

	return p
	
def bin(x):
	return round(x*20)/20

def roundToTheNearestBillion(x):
	return round(x/10**9)*10**9

def roundToTheNearestMillion(x):
	return round(x/10**6)*10**6
