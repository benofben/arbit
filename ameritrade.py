import urllib
import xmltodict
import constants

versionnumber='1.0'
baseurl='https://apis.tdameritrade.com/apps/100/'

class ameritrade(object):
	jessionid = None

	def LogIn(self):
		url = baseurl + 'LogIn?source=' + constants.sourceID + '&version=' + versionnumber
		params=urllib.urlencode({'userid': constants.userid, 'password': constants.password, 'source': constants.sourceID, 'version': versionnumber})
		f = urllib.urlopen(url, params)
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		
		self.jsessionid = d['xml-log-in'][0]['session-id'][0]
		
		return d

	def LogOut(self):
		url = baseurl + 'LogOut;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID
		f = urllib.urlopen(url)
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d

	def KeepAlive(self):
		url = 'https://apis.tdameritrade.com/apps/KeepAlive;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID
		f = urllib.urlopen(url)
		response = f.read()
		return response

	def BalancesAndPositions(self):
		url = baseurl + 'BalancesAndPositions;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID
		params=urllib.urlencode({'source': constants.sourceID})
		f = urllib.urlopen(url)
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d

	def SnapshotQuotes(self, symbol):
		url = baseurl + 'Quote;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID + '&symbol=' + symbol
		params=urllib.urlencode({'source': constants.sourceID})
		f = urllib.urlopen(url)
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d

	def EquityTrade(self, orderstring):
		url = baseurl + 'EquityTrade;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID + '&orderstring=' + orderstring
		params=urllib.urlencode({'source': constants.sourceID})
		f = urllib.urlopen(url)
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d
	
	def OrderStatus(self, orderid):
		url = baseurl + 'OrderStatus;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID + '&orderid=' + orderid
		params=urllib.urlencode({'source': constants.sourceID})
		f = urllib.urlopen(url)
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d