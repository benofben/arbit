import urllib.request
import urllib.parse
import xmltodict
import constants

versionnumber='1.0'
baseurl='https://apis.tdameritrade.com/apps/100/'

import struct
def bytesToBool(b):
	i = struct.unpack('?', b)[0]
	return i

def bytesToInt(b):
	i = struct.unpack('!i', b)[0]
	return i

def bytesToShort(b):
	i = struct.unpack('!h', b)[0]
	return i

def bytesToLong(b):
	i = struct.unpack('!q', b)[0]
	return i

def bytesToFloat(b):
	i = struct.unpack('!f', b)[0]
	return i

class ameritrade(object):
	jessionid = None

	def LogIn(self):
		url = baseurl + 'LogIn?source=' + constants.sourceID + '&version=' + versionnumber
		params=urllib.parse.urlencode({'userid': constants.userid, 'password': constants.password, 'source': constants.sourceID, 'version': versionnumber})
		
		try:
			f = urllib.request.urlopen(url, params)
		except IOError:
			return None
		
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		
		self.jsessionid = d['xml-log-in'][0]['session-id'][0]
		
		return d

	def LogOut(self):
		url = baseurl + 'LogOut;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID
		
		try:
			f = urllib.request.urlopen(url)
		except IOError:
			return None
		
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d

	def KeepAlive(self):
		url = 'https://apis.tdameritrade.com/apps/KeepAlive;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID
		
		try:
			f = urllib.request.urlopen(url)
		except IOError:
			return None
		
		response = f.read()
		return response

	def SnapshotQuotes(self, symbol):
		url = baseurl + 'Quote;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID + '&symbol=' + symbol
		params=urllib.parse.urlencode({'source': constants.sourceID})
		
		try:
			f = urllib.request.urlopen(url)
		except IOError:
			return None
		
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d

	def PriceHistory(self, symbol, date):
		url = baseurl + 'PriceHistory;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID + '&requestidentifiertype=SYMBOL&requestvalue=' + symbol + '&intervaltype=MINUTE&intervalduration=1&extended=true&startdate=' + date + '&enddate=' + date
		params=urllib.parse.urlencode({'source': constants.sourceID})
		
		try:
			f = urllib.request.urlopen(url)
		except IOError:
			return None
		
		d = f.read()
		
		i=0
		symbolCount=bytesToInt(d[i:i+4])
		i+=4
		
		if symbolCount!=1:
			# then something screwy is going on, and we have an error
			# the first two bytes are mysterious, the rest is an error message
			#print ''.join([hex(ord(x))[2:] for x in d[0:2]]) + ': ' + d[2:]
			return None
		
		# if we got here, then there should be something to parse...
		
		symbolLength=bytesToShort(d[i:i+2])
		i+=2
		
		symbol=d[i:i+symbolLength]
		i+=symbolLength
		
		errorCode=bytesToBool(d[i:i+1])
		i+=1
		
		if errorCode:
			errorLength=bytesToShort(d[i:i+2])
			i+=2
			
			errorText=d[i:i+errorLength]
			i+=errorLength
			
			print (errorText + 'hi')
			return None
		
		barCount=bytesToInt(d[i:i+4])
		i+=4
		
		data = {}
		data['Close']=[]
		data['High']=[]
		data['Low']=[]
		data['Open']=[]
		data['Volume']=[]
		data['TimeStamp']=[]
		
		for bar in range(0, barCount):
			data['Close'].append(bytesToFloat(d[i:i+4]))
			i+=4
			
			data['High'].append(bytesToFloat(d[i:i+4]))
			i+=4
			
			data['Low'].append(bytesToFloat(d[i:i+4]))
			i+=4
			
			data['Open'].append(bytesToFloat(d[i:i+4]))
			i+=4
			
			# volume is 100x greater than this number
			volume = round(bytesToFloat(d[i:i+4]))*100
			data['Volume'].append(volume)
			i+=4
			
			data['TimeStamp'].append(bytesToLong(d[i:i+8]))
			i+=8
		
		return data

	def BalancesAndPositions(self):
		url = baseurl + 'BalancesAndPositions;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID
		params=urllib.parse.urlencode({'source': constants.sourceID})
		
		try:
			f = urllib.request.urlopen(url)
		except IOError:
			return None
		
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d

	def OrderStatus(self, orderid):
		url = baseurl + 'OrderStatus;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID + '&orderid=' + orderid
		params=urllib.parse.urlencode({'source': constants.sourceID})
		
		try:
			f = urllib.request.urlopen(url)
		except IOError:
			return None
		
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d

	def EquityTrade(self, orderstring):
		url = baseurl + 'EquityTrade;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID + '&orderstring=' + orderstring
		params=urllib.parse.urlencode({'source': constants.sourceID})
		try:
			f = urllib.request.urlopen(url)
		except IOError:
			return None
		
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d

	def EditOrder(self, orderstring):
		url = baseurl + 'EditOrder;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID + '&orderstring=' + orderstring
		params=urllib.parse.urlencode({'source': constants.sourceID})
		
		try:
			f = urllib.request.urlopen(url)
		except IOError:
			return None
		
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d

	def OrderCancel(self, orderid):
		url = baseurl + 'OrderCancel;jsessionid=' + self.jsessionid + '?source=' + constants.sourceID + '&orderid=' + orderid
		params=urllib.parse.urlencode({'source': constants.sourceID})
		
		try:
			f = urllib.request.urlopen(url)
		except IOError:
			return None
		
		xmlstring = f.read()
		d=xmltodict.xmltodict(xmlstring)
		return d
