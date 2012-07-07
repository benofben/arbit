dataDirectory='C:/arbitdata/'

import datetime
trainingStartDate = datetime.date.today() - datetime.timedelta(days=300)
trainingEndDate = datetime.date.today() - datetime.timedelta(days=50)
testStartDate = datetime.date.today() - datetime.timedelta(days=49)
testEndDate = datetime.date.today()
