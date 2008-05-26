import sys	# for maxint
import data

class classifier:
	def __init__(self, symbol, currentDate, quotes):
		self.symbol=symbol
		self.currentDate=currentDate
		self.quotes=quotes

	def run(self):
		[trainingSet, testPoint]=self.createDataSet()
		p=self.naiveBayes(trainingSet, testPoint)
		return p

	def naiveBayes(self, trainingSet, testPoint):
		if not trainingSet or not len(trainingSet)>0:
			return False

		classes=['Good', 'Bad']

		# compute p(C|F_1, F_2, ... F_n)
		p={}
		for C in classes:
			# compute p(C)
			p[C]=0
			for i in range(0, len(trainingSet)):
				if trainingSet[i]['Outcome']==C:
					p[C]=p[C]+1.0
			p[C]=p[C]/len(trainingSet)

			# allocate arrays for p(F_i|C) and count(F_i|C)
			pFC={}
			FtC={}
			for predictor in testPoint:
				if predictor!='Outcome':
					pFC[predictor]=0
					FtC[predictor]=0

			# compute p(F_i|C)
			for i in range(0, len(trainingSet)):
				if trainingSet[i]['Outcome']==C:
					for predictor in trainingSet[i]:
						if predictor!='Outcome':
							if trainingSet[i][predictor]==testPoint[predictor]:
								pFC[predictor]=pFC[predictor]+1
							FtC[predictor]=FtC[predictor]+1

			# compute p(C) * Pi[p(F_i|C)]
			for predictor in pFC:
				if pFC[predictor]!=0:
					pFC[predictor]=float(pFC[predictor])/FtC[predictor]
				p[C]=p[C]*pFC[predictor]

		# allocate arrays for p(F_i) and count(F_i)
		pF={}
		Ft={}
		for predictor in testPoint:
			if predictor!='Outcome':
				pF[predictor]=0
				Ft[predictor]=0

		# compute p(F_i)
		for i in range(0, len(trainingSet)):
			for predictor in trainingSet[i]:
				if predictor!='Outcome':
					if trainingSet[i][predictor]==testPoint[predictor]:
						pF[predictor]=pF[predictor]+1
					Ft[predictor]=Ft[predictor]+1

		# compute Pi[p(F_i)]
		pi=1
		for predictor in pF:
			if pF[predictor]!=0:				pF[predictor]=float(pF[predictor])/Ft[predictor]
			pi=pi*pF[predictor]

		# compute p(C|F_1, F_2, ... F_n) = p(C) * Pi[p(F_i|C)] / Pi[p(F_i)]
		for C in classes:
			if pi!=0 and p[C]!=0:
				p[C]=p[C]/pi
	
		return p

	def createDataSet(self):
		# the key value is the window to use the predictor for
		predictors = {'Symbol':5, 'xDayHigh':100, 'xDayLow':100}

		# create the training set
		trainingSet=[]
		for symbol in self.quotes:
			currentIndex=data.getIndex(self.currentDate, self.quotes[symbol])
			if currentIndex and currentIndex-105>0:

				# add a data point for each predictor and day
				for predictor in predictors:
					window=predictors[predictor]
					for day in range(currentIndex-window, currentIndex):
						trainingSet.append(self.createDataPoint(day, symbol, predictor))

		# create a test point
		testPoint={}
		day=data.getIndex(self.currentDate, self.quotes[self.symbol])

		for predictor in predictors:
			point=self.createDataPoint(day, self.symbol, predictor)
			testPoint[predictor]=point[predictor]

		return [trainingSet, testPoint]

	def createDataPoint(self, day, symbol, predictor):
		dataPoint={}

		if predictor=='Symbol':
			dataPoint['Symbol']=symbol
		elif predictor=='xDayHigh':
			# last closing price was x% of the y day high
			High=0
			for i in range(day-4, day+1):
				if self.quotes[symbol]['High'][i]>High:
					High=self.quotes[symbol]['High'][i]
			Last=self.quotes[symbol]['Close'][day]
			dataPoint['xDayHigh']=self.bin(Last/High)
		elif predictor=='xDayLow':
			# last closing price was x% of the y day low
			Low=sys.maxint
			for i in range(day-4, day+1):
				if self.quotes[symbol]['Low'][i]<Low:
					Low=self.quotes[symbol]['Low'][i]
			Last=self.quotes[symbol]['Close'][day]
			dataPoint['xDayLow']=self.bin(Last/Low)
		else:
			print 'I found an unrecognized predictor: ' + predictor \
			+ '. This means there is an error in your code.'

		# populate the outcome for today if we have data
		if len(self.quotes[symbol]['High'])>day+1 \
			and self.quotes[symbol]['High'][day+1]>self.quotes[symbol]['Open'][day+1]*1.02:
			dataPoint['Outcome']='Good'
		else:
			dataPoint['Outcome']='Bad'

		return dataPoint

	def bin(self, x):
		return round(x*20)/20
