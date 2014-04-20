
def getAnalysisForDate(currentDate, mySql):

	#skip if we already have data for this day
	upgrades = mySql.fetch(currentDate, 'Upgrade')
	downgrades = mySql.fetch(currentDate, 'Downgrade')
	if upgrades or downgrades:
		print ('Skipping download for ' + currentDate.isoformat())
		return
	
	data = downloadUpgradeForDate(currentDate)	
	upgrades = parseForDate(data, currentDate, 'Upgrade')
	for upgrade in upgrades:
		mySql.insert(upgrade)

	data = downloadDowngradeForDate(currentDate)	
	downgrades = parseForDate(data, currentDate, 'Downgrade')
	for downgrade in downgrades:
		mySql.insert(downgrade)
	
def downloadUpgradeForDate(currentDate):
	directory = '/Investor/Calendars/Upgrades-Downgrades/Upgrades/'
	return downloadForDate(currentDate, directory)

def downloadDowngradeForDate(currentDate):
	directory = '/Investor/Calendars/Upgrades-Downgrades/Downgrades/'
	return downloadForDate(currentDate, directory)

def downloadForDate(currentDate, directory):
	year = currentDate.strftime('%Y')
	month = currentDate.strftime('%m')
	day = currentDate.strftime('%d')
	
	import http.client
	conn = http.client.HTTPConnection('briefing.com')

	conn.request('GET', directory + year + '/' + month + '/' + day)
	response=conn.getresponse()
	print(response.status, response.reason)
	data=response.read()
	conn.close()

	if response.status==200 and response.reason=='OK':
		print('Analyst download succeeded for ' + currentDate.isoformat())
		data = data.decode('utf8')
		return data
	else:
		print('Analyst download failed for ' + currentDate.isoformat())
		return False
	
def parseForDate(data, currentDate, changeType):
	# throw away everything before:
	# <td class="padding-left5" style="width:100px;">Price Target</td>
	data = data.split('<td class="padding-left5" style="width:100px;">Price Target</td>')
	if (len(data)<2):
		# then there were no upgrades today
		return []
	data = data[1]
	
	# throw away everything after:
	# </table>
	data = data.split('</table>')
	data = data[0]
	
	# now we split on </tr>.  Each </tr> is an analyst upgrade
	data = data.split('</tr>')
	
	parsedChanges = []
	for analystChange in data:
		parsedChange = parseChange(analystChange, currentDate, changeType)
		if(parsedChange):
			parsedChanges.append(parsedChange)
	
	return parsedChanges

def parseChange(analystChange, currentDate, changeType):
	analystChange = analystChange.split('<td class="')
	
	if(len(analystChange)==6):
		#then this is an upgrade, not header information
		
		parsedChange = {}
		parsedChange['RatingsChangeDate'] = currentDate
		parsedChange['RatingsChangeType'] = changeType
		
		company = analystChange[1]
		company = company.replace('td-dot-border" style="width:180px;">','')
		company = company.replace('</td>','')
		company = company.strip()
		parsedChange['Company'] = company
		
		ticker = analystChange[2]
		ticker = ticker.replace('"><a class="ticker" href="/investor/search/search.aspx?ticker=','')
		ticker = ticker.replace('</a></td>','')
		ticker = ticker.split('">')
		ticker = ticker[1]
		ticker = ticker.strip()
		parsedChange['Ticker'] = ticker
		
		brokerageFirm = analystChange[3]
		brokerageFirm = brokerageFirm.replace('td-dot-border" style="width:200px;">', '')
		brokerageFirm = brokerageFirm.replace('</td>', '')
		brokerageFirm = brokerageFirm.replace('&amp;', '&')
		brokerageFirm = brokerageFirm.strip()
		parsedChange['BrokerageFirm'] = brokerageFirm
		
		ratingsChange = analystChange[4]
		ratingsChange = ratingsChange.replace('td-dot-border" style="width:160px;">', '')
		ratingsChange = ratingsChange.replace('</td>', '')
		ratingsChange = ratingsChange.replace('<b> &#187;', ' to')
		ratingsChange = ratingsChange.replace('</b>', '')
		ratingsChange = ratingsChange.strip()
		parsedChange['RatingsChange'] = ratingsChange
		
		priceTarget = analystChange[5]
		priceTarget = priceTarget.replace('padding-left5">','')
		priceTarget = priceTarget.replace('</td>','')
		priceTarget = priceTarget.replace('&#187;','to')
		priceTarget = priceTarget.replace('<br>', '')
		priceTarget = priceTarget.strip()
		parsedChange["PriceTarget"] = priceTarget
		
		return parsedChange
	return False
	