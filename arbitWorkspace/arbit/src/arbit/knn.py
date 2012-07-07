import datetime
import random
import sys

n=3

def classify(testPoint, trainingPoints):
	[normalizedTestPoint, normalizedTrainingPoints] = normalize(testPoint, trainingPoints)
	
	bestPoints = []
	for unused_i in range(0,n):
		bestPoint = {}
		bestPoint['Distance'] = sys.maxsize
		bestPoint['Outcome'] = ''
		bestPoints.append(bestPoint)
	
	for i in range(0,len(normalizedTrainingPoints['Outcome'])):
		d = distance(normalizedTestPoint, normalizedTrainingPoints, i)

		if d<bestPoints[n-1]['Distance']:
			bestPoints[n-1]['Distance'] = d
			bestPoints[n-1]['Outcome'] = normalizedTestPoint['Outcome']
			bestPoints = sorted(bestPoints, key=lambda k: k['Distance'])
		
	return (random.random()*2)-1
	
def distance(testPoint, trainingPoint, i):
	d=0
	
	for key in testPoint.keys():
		if key != 'Outcome':
			if isinstance(trainingPoint[key][i], str):
				if trainingPoint[key][i] != testPoint[key][0]:
					d = d + 2 ** 2		
			elif isinstance(trainingPoint[key][i], int) or isinstance(trainingPoint[key][i], float):
				d = d + (trainingPoint[key][i]-testPoint[key][0]) ** 2
			else:
				pass
				#print('I do not know how to compute distance for type ' + str(type(testPoint[key][0])))
	
	d = d ** (1/2)
	return d

def normalize(testPoint, trainingPoints):
	'''
	So, we want to create normalized data where mean=0 and var=1
	
	This is all going to feed into a knn classifier.  
	This means that for discrete data such as Industry and Sector our distance will always be 2.
	
	For data which is approximately normally distributed such as high, low, close, we can simply scale.
	
	For marketcap, it may make sense to take log(marketCap) and then scale so that mega caps do not bias the sample.
	
	We want to put the normalizer in the knn code because we will normalize separately for each training set.  
	We'll do this on demand rather than to the DB.
	'''
	
	normalizedTestPoint = {}
	normalizedTrainingPoints = {}
	
	for key in trainingPoints.keys():
		if key == 'Return':
			# Drop the return data, so we don't pretidct on things we shouldn't know
			pass
		elif isinstance(trainingPoints[key][0], str):
			# We don't need to do anything for a string, including Outcome
			normalizedTrainingPoints[key] = trainingPoints[key]
			normalizedTestPoint[key] = testPoint[key]
		elif isinstance(trainingPoints[key][0], int) or isinstance(trainingPoints[key][0], float):
			[normalizedTrainingPoints[key], normalizedTestPoint[key]] = normalizeNumber(trainingPoints[key], testPoint[key])
		elif isinstance(trainingPoints[key][0], datetime.datetime):
			[normalizedTrainingPoints[key], normalizedTestPoint[key]] = normalizeDateTime(trainingPoints[key], testPoint[key])
		else:
			print('I do not know how to normalize for type ' + str(type(trainingPoints[key][0])))
	
	return [normalizedTestPoint, normalizedTrainingPoints]

def normalizeDateTime(trainingPoints, testPoint):
	normalizedTrainingPoints=[]
	normalizedTestPoint=[]
	
	startDate = trainingPoints[0]
	for date in trainingPoints:
		x = (date-startDate).days
		normalizedTrainingPoints.append(x)
	
	x = (testPoint[0]-startDate).days
	normalizedTestPoint.append(x)
	
	[normalizedTrainingPoints, normalizedTestPoint] = normalizeNumber(normalizedTrainingPoints, normalizedTestPoint)
	return [normalizedTrainingPoints, normalizedTestPoint]

def normalizeNumber(trainingPoints, testPoint):
	normalizedTrainingPoints=[]
	normalizedTestPoint=[]
	
	# compute sample mean
	mean = 0
	for point in trainingPoints:
		mean = mean + point
	mean = mean / len(trainingPoints)
	
	# compute sample variance
	variance = 0
	for point in trainingPoints:
		variance = variance + ((point - mean) ** 2)
	variance = variance /len(trainingPoints)
	standardOfDeviation = variance ** (1/2)
	
	if standardOfDeviation == 0:
		standardOfDeviation = 1
	
	# normalize the training points
	for point in trainingPoints:
		point = (point - mean)/standardOfDeviation
		normalizedTrainingPoints.append(point)
		
	# normalize the test point
	point = (testPoint[0] - mean)/standardOfDeviation
	normalizedTestPoint.append(point)
			
	return [normalizedTrainingPoints, normalizedTestPoint]

