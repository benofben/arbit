capital = 0

for year in range(2011, 2011+65-30):
	for month in range(0,12):
		capital *= 1 + 0.15/12
		capital += 1000	
	print(str(year) + ' ' + str(month) + ' ' + str(capital))
	