import quotesYahoo
import datetime

class knn:
	quotes=quotesYahoo.getAllQuotes()
	
	def __init__(self):
		capital=10000
		leverage=2
		
		startDate = datetime.date(2009,10,1)
		endDate = datetime.date.today()
		
		currentDate=startDate
		while currentDate<endDate:
			
			points=self.getPoints(currentDate)
			if points:
				[trainingPoints, testingPoints]=points
			else:
				trainingPoints=[]
				testingPoints=[]
				
			bestR=0
			bestSymbol=None
			
			for testingPoint in testingPoints:
				r=self.evaluate(trainingPoints, testingPoint)
				if(r>bestR):
					bestR=r
					bestSymbol=testingPoint[len(testingPoint)-1]
			
			if bestSymbol:
				q=quotesYahoo.getSubquoteForSymbol(bestSymbol, currentDate, self.quotes)
				actualR=q['Close'][len(q['Close'])-1]/q['Open'][len(q['Open'])-1]
				capital=capital*(((actualR-1)*leverage)+1)
				print(str(currentDate) + '\t' + bestSymbol + '\t' + str(capital) + '\t' + str(bestR) + '\t' + str(actualR))
			
			currentDate=currentDate+datetime.timedelta(days=1)
	
	def evaluate(self, trainingPoints, testingPoint):
		# Find the points closest to testingPoint in our weird geometry
		closestPoints=[]
		for p in trainingPoints:
			d=self.distance(p, testingPoint)
			closestPoints.append([d,p])
			closestPoints.sort(reverse=True)
			if len(closestPoints)>100:
				closestPoints.pop()
		
		# Compute the cummulative return on the closest points
		r=1
		for p in closestPoints:
			r=r*p[0]
			r=r**(1/10)
		
		return r
	
	def distance(self, pointA, pointB):
		d=0
		for i in range(1,len(pointA)-1):
			d=d+abs(pointA[i]-pointB[i])
		if pointA[len(pointA)-1]!=pointB[len(pointB)-1]:
			d=d+1
		return d
	
	def getPoints(self, currentDate):
		q=quotesYahoo.getSubquote(currentDate, self.quotes)
		if not q:
			return False
	
		trainingPoints=[]
		testingPoints=[]
		
		for symbol in q:
			for i in range(len(q[symbol]['Open'])-50,len(q[symbol]['Open'])):
				p=[]
				p.append(q[symbol]['Close'][i]/q[symbol]['Open'][i])
				p.append(q[symbol]['Close'][i-1]/q[symbol]['Open'][i-1])
				p.append(q[symbol]['Close'][i-2]/q[symbol]['Open'][i-2])
				
				try:
					p.append((q[symbol]['Volume'][i-2]-q[symbol]['Volume'][i-1])/(q[symbol]['Volume'][i-2]+q[symbol]['Volume'][i-1]))
				except ZeroDivisionError:
					p.append(0)
				
				p.append(symbol)
				
				if i<len(q[symbol]['Open'])-1:
					trainingPoints.append(p)
				else:
					testingPoints.append(p)
				
		return[trainingPoints, testingPoints]

knn()