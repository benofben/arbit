import arbit.sql

class simulate:

	def __init__(self):
		arbitSql = arbit.sql.sql()
		classifications = arbitSql.fetchClassifications()
		
		capital = 25000
		print('0000-00-00T00:00:00' + '\t\t\t\t' + str(capital))
		for i in range(0, len(classifications['CurrentTestDate'])):
			capital = capital * classifications['Return'][i]
			print(classifications['CurrentTestDate'][i].isoformat() + '\t' + classifications['Outcome'][i] + '\t' + classifications['Symbol'][i] + '\t' + str(classifications['Return'][i]) + '\t' + str(capital) )