import symbols
import quotes
import data
import sys
from svm import *

import datetime
startDate=datetime.date(2008,1,1)
endDate=datetime.date.today()

take=0.02

def download():
	symbols.downloadSymbols()
	quotes.downloadAllQuotes()

def download_ibs_bucket():
	symbols=['C','CS','DB','GS','LEH','MER','RY','UBS','WB','HBC']
	for symbol in symbols:
	    quotes.downloadQuotes(symbol)

def getLabel(quotes, day, symbol):
	# get today's label if we have data
	if day+1>=len(quotes[symbol]['Open']):
		return False
       	if quotes[symbol]['Low'][day+1]<quotes[symbol]['Open'][day+1]*(1-take):
       		return 1
	else:
       		return -1

def getSample(quotes, day, symbol):
	# get today's sample if we have data
	if day>=len(quotes[symbol]['Open']) or day-4<0:
		return False

	sample=[]

	# each symbol gets its own dimension
	for s in quotes:
		if s!=symbol:
			sample.append(0)
		else:
			sample.append(1)

	# last closing price was x% of the y day high
	High=0
	for i in range(day-4, day+1):
		if quotes[symbol]['High'][i]>High:
			High=quotes[symbol]['High'][i]
	Last=quotes[symbol]['Close'][day]
	yDayHigh=Last/High
	yDayHigh=10.0*(yDayHigh-1.0)
	sample.append(yDayHigh)

	# last closing price was x% of the y day low
	Low=sys.maxint
	for i in range(day-4, day+1):
		if quotes[symbol]['Low'][i]<Low:
			Low=quotes[symbol]['Low'][i]
	Last=quotes[symbol]['Close'][day]
	yDayLow=Last/Low
	yDayLow=10.0*(yDayLow-1.0)
	sample.append(yDayLow)

	return sample

def getDataSet(quotes, currentDate):
	# the test samples all come from currentDate
	# training samples come from older data
	window = 100

	trainingLabels=[]
	trainingSamples=[]
	testSamples=[]

	for symbol in quotes:
		currentIndex=data.getIndex(currentDate, quotes[symbol])
		if currentIndex and currentIndex-window>0:
			for day in range(currentIndex-window, currentIndex):
				label=getLabel(quotes, day, symbol)
				sample=getSample(quotes, day, symbol)
				if label and sample:
					trainingLabels.append(label)
					trainingSamples.append(sample)

		testSamples.append(getSample(quotes, currentIndex, symbol))	

	return [trainingLabels, trainingSamples, testSamples]

def run():
	c=25000
	wins=0
	total=0

	symbols=data.getSymbols()
	quotes=data.getAllQuotes()
	print 'Finished loading quotes.'

	for day in range(0, (endDate-startDate).days+1):
		currentDate=startDate+datetime.timedelta(days=day)
		[trainingLabels, trainingSamples, testSamples] = getDataSet(quotes, currentDate)
	
		if trainingLabels and trainingSamples and testSamples:
			parameters = svm_parameter(kernel_type = LINEAR, C = 10)
			problem = svm_problem(trainingLabels, trainingSamples)
			model = svm_model(problem, parameters)
		
			predictedTestLabels=[]
			for testSample in testSamples:
				r = model.predict_values_raw(testSample)
				predictedTestLabels.append(r[0])

			# now test against the next day's result if we have data
			symbol=symbols[predictedTestLabels.index(max(predictedTestLabels))]
			currentIndex=data.getIndex(currentDate, quotes[symbol])
			if currentIndex+1<len(quotes[symbol]['Open']):
				Open=quotes[symbol]['Open'][currentIndex+1]
				Low=quotes[symbol]['Low'][currentIndex+1]
				Close=quotes[symbol]['Close'][currentIndex+1]

			       	if Low<Open*(1-take):
					delta=2*c*take
					wins=wins+1
				else:
					delta=2*(c*Open/Close-c)
				c=c+delta
				total=total+1				
			else:
				# we don't have data, so this must be the final point
				delta=0

			print str(currentDate) + '\t' + symbol + '\t' + str(max(predictedTestLabels)) + '\t' + str(c) + '\t' + str(delta) + '\t' + str(float(wins)/total)
run()

