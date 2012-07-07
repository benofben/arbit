
def getUpgradesForDate(currentDate, mySql):

	# skip if we already have data for this day
	upgrades = mySql.fetch(currentDate)
	if upgrades:
		print ('Skipping download for ' + currentDate.isoformat())
		return
	
	data = downloadForDate(currentDate)	
	upgrades = parseUpgradesForDate(data, currentDate)
	for upgrade in upgrades:
		mySql.insert(upgrade)
	
def downloadForDate(currentDate):
	year = currentDate.strftime('%Y')
	month = currentDate.strftime('%m')
	day = currentDate.strftime('%d')
	
	import http.client
	conn = http.client.HTTPConnection('briefing.com')

	conn.request('GET', '/Investor/Calendars/Upgrades-Downgrades/Upgrades/' + year + '/' + month + '/' + day)
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
	
def parseUpgradesForDate(data, currentDate):
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
	
	parsedUpgrades = []
	for analystUpgrade in data:
		parsedUpgrade = parseUpgrade(analystUpgrade, currentDate)
		if(parsedUpgrade):
			parsedUpgrades.append(parsedUpgrade)
	
	return parsedUpgrades

def parseUpgrade(analystUpgrade, currentDate):
	analystUpgrade = analystUpgrade.split('<td class="')
	
	if(len(analystUpgrade)==6):
		#then this is an upgrade, not header information
		
		parsedUpgrade = {}
		parsedUpgrade['RatingsChangeDate'] = currentDate
		
		company = analystUpgrade[1]
		company = company.replace('td-dot-border" style="width:180px;">','')
		company = company.replace('</td>','')
		company = company.strip()
		parsedUpgrade['Company'] = company
		
		ticker = analystUpgrade[2]
		ticker = ticker.replace('"><a class="ticker" href="/investor/search/search.aspx?ticker=','')
		ticker = ticker.replace('</a></td>','')
		ticker = ticker.split('">')
		ticker = ticker[1]
		ticker = ticker.strip()
		parsedUpgrade['Ticker'] = ticker
		
		brokerageFirm = analystUpgrade[3]
		brokerageFirm = brokerageFirm.replace('td-dot-border" style="width:200px;">', '')
		brokerageFirm = brokerageFirm.replace('</td>', '')
		brokerageFirm = brokerageFirm.replace('&amp;', '&')
		brokerageFirm = brokerageFirm.strip()
		parsedUpgrade['BrokerageFirm'] = brokerageFirm
		
		ratingsChange = analystUpgrade[4]
		ratingsChange = ratingsChange.replace('td-dot-border" style="width:160px;">', '')
		ratingsChange = ratingsChange.replace('</td>', '')
		ratingsChange = ratingsChange.replace('<b> &#187;', ' to')
		ratingsChange = ratingsChange.replace('</b>', '')
		ratingsChange = ratingsChange.strip()
		parsedUpgrade['RatingsChange'] = ratingsChange
		
		priceTarget = analystUpgrade[5]
		priceTarget = priceTarget.replace('padding-left5">','')
		priceTarget = priceTarget.replace('</td>','')
		priceTarget = priceTarget.replace('&#187;','to')
		priceTarget = priceTarget.replace('<br>', '')
		priceTarget = priceTarget.strip()
		parsedUpgrade["PriceTarget"] = priceTarget
		
		return parsedUpgrade
	return False
	