# for maxint
import sys
import data

class classifier:
	def __init__(self, symbol, currentDate, quotes):
		self.symbol=symbol
		self.currentDate=currentDate
		self.quotes=quotes

	def run(self):
		[trainingSet, testPoint]=self.createDataSet()
		p=self.naiveBayesClassify(trainingSet, testPoint)
		return p

	def naiveBayesClassify(self, trainingSet, testPoint):
		if not trainingSet or not len(trainingSet)>0:
			return False
	
		classes=['Good', 'Bad']
		
		# compute p(C|F_1, F_2, ... F_n)
		p={}
		for C in classes:
			# compute p(C)
			p[C]=0
			for day in range(0, len(trainingSet)):
				if trainingSet[day]['Outcome']==C:
					p[C]=p[C]+1.0
			p[C]=p[C]/len(trainingSet)

			# allocate two arrays
			pF=[]
			Ft=[]
			for i in trainingSet[0]:
				if i!='Outcome':
					for j in range(0,len(trainingSet[0][i])):
						pF.append(0)
						Ft.append(0)

			# compute p(F_i|C)
			for day in range(0, len(trainingSet)):
				if trainingSet[day]['Outcome']==C:
					index=0
					for i in trainingSet[day]:
						if i!='Outcome':
							for j in range(0,len(trainingSet[day][i])):
								if trainingSet[day][i][j]==testPoint[i][j]:
									pF[index]=pF[index]+1
								Ft[index]=Ft[index]+1
								index=index+1

			# compute p(C|F_1, F_2, ... F_n) = p(C) * Pi[p(F_i|C)]
			for i in range(0,len(pF)):
				if pF[i]!=0:
					pF[i]=float(pF[i])/Ft[i]
				else:
					pF[i]=0.01
				p[C]=p[C]*pF[i]

		# scale p(C) by 1/Z
		Z=0
		for C in p:
			Z=Z+p[C]
		for C in p:
			p[C]=p[C]/Z
			
		return p

	def createDataSet(self):
		# create the training set
		trainingWindow=100
		trainingSet=[]
		for symbol in self.quotes:
			currentIndex=data.getIndex(self.currentDate, self.quotes[symbol])
			if currentIndex and currentIndex-trainingWindow-5>0:
				for day in range(currentIndex-trainingWindow, currentIndex):
					trainingSet.append(self.createDataPoint(day, symbol))

		# create a test point
		day=data.getIndex(self.currentDate, self.quotes[self.symbol])
		testPoint=self.createDataPoint(day, self.symbol)
					   
		return [trainingSet, testPoint]

	def createDataPoint(self, day, symbol):
		# add the symbol
		dataPoint={}
		dataPoint['Symbol']=[]
		dataPoint['Symbol'].append(symbol)

		# last closing price was x% of the y day high, low
		High=0
		Low=sys.maxint
		for i in range(day-4, day+1):
			if self.quotes[symbol]['High'][i]>High:
				High=self.quotes[symbol]['High'][i]
			if self.quotes[symbol]['Low'][i]<Low:
				Low=self.quotes[symbol]['Low'][i]
		dataPoint['xDay']=[]
		Last=self.quotes[symbol]['Close'][day]
		dataPoint['xDay'].append(self.bin(Last/High))
		dataPoint['xDay'].append(self.bin(Last/Low))

		# populate the outcome for today if we have data
		if len(self.quotes[symbol]['High'])>day+1 \
			and self.quotes[symbol]['High'][day+1]>self.quotes[symbol]['Open'][day+1]*1.02:
			dataPoint['Outcome']='Good'
		else:
			dataPoint['Outcome']='Bad'

		return dataPoint

	def bin(self, x):
		return round(x*20)/20
