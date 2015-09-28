filename = '/home/ec2-user/sk/probabilities.test'
f = open(filename, 'r')
p=[]
for line in f:
	x=line.replace('\n','')
	x=float(x)
	p.append(x)

#### get dates from the test file
filename = '/home/ec2-user/sk/test.data'
f = open(filename, 'r')
d=[]
s=[]
for line in f:
	x=line.split(',')
	date=x[0]
	y=x[2]
	if date != 'date':
		d.append(date)
		s.append(y)

filename = '/home/ec2-user/sk/labels.test'
f = open(filename, 'r')
l=[]
for line in f:
	x=line.replace('\n','')
	x=float(x)
	l.append(x)

assert(len(p)==len(d))
assert(len(l)==len(d))

# print our predictions
outputFilename = 'testPredictions.csv'
f = open(outputFilename, 'w')
for i in range(0,len(p)):
	if(l[i]==1):
		probability=p[i]
	else:
		probability=0

	f.write(str(d[i]) + ',' + s[i] + ',' + str(probability) + '\n')
