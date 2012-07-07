import nasdaq.sql
import yahoo.sql
import yahoo.quotes
import constants

import datetime

def run():	
	print('Loading quotes from database...')
	yahooSql = yahoo.sql.sql()
	quotes = yahooSql.fetchInformation(constants.trainingStartDate, constants.testEndDate)
	symbols = yahoo.quotes.getUniqueList(quotes['Symbol'])
	quotes = yahoo.quotes.reformatQuotes(quotes, symbols)
	
	nasdaqSql = nasdaq.sql.sql()
	nasdaqInformation = nasdaqSql.fetchInformation()
	print('Done loading.')
	
	print('Making points...')
	trainingPoints = getDataPoints(quotes, nasdaqInformation, constants.trainingStartDate, constants.trainingEndDate)
	testPoints = getDataPoints(quotes, nasdaqInformation, constants.testStartDate, constants.testEndDate)
	print('Done making points.')
	
	print('Writing points to filesystem...')
	writePoints('trainingPoints.csv', trainingPoints)
	writePoints('testPoints.csv', testPoints)
	print('Done writing points to filesystem.')

def writePoints(filename, points):
	file = open(constants.dataDirectory + filename, 'w')

	# write header	
	file.write('label')
	for i in range(1,len(points[0])):
		file.write(', predictor' + str(i)) 
	file.write('\n')

	# write data
	for point in points:
		file.write(str(point[0]))
		for i in range(1, len(points[0])):
			file.write(', ' + str(point[i]))
		file.write('\n')
	
	file.close()

def getDataPoints(quotes, nasdaqInformation, startDate, endDate):
	points = []
	
	for symbol in nasdaqInformation:
		currentDate = startDate		
		while currentDate <= endDate:
			try:
				point = getPoint(currentDate, quotes[symbol])
			except KeyError:
				pass
			
			if point:
				#for predictor in nasdaqInformation[symbol]:
				#	point.append(predictor)
				point.append(currentDate)
				point.append(symbol)
				points.append(point)
			currentDate = currentDate + datetime.timedelta(days=1)

	return points
	
def getPoint(date, quotes):
	point=[]
	
	i = yahoo.quotes.getIndex(date, quotes)
	if i and i>100:
		# then we have enough data to make a training point
		# label is first element
		# then we have a bunch of predictors
		total=0
		wins=0
		for j in range(0,100):			
			k = i-j
			if j==0:
				if quotes['High'][k]>quotes['Open'][k]*1.02:
					point.append('W')
				else:
					point.append('L')
			else:
				total = total + 1
				if quotes['High'][k]>quotes['Open'][k]*1.02:
					wins = wins+1
				point.append(wins/total)
				
	return point