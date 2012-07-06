from html.parser import HTMLParser
import urllib.request

class MyHTMLParser(HTMLParser):
	def __init__(self, symbol):
		HTMLParser.__init__(self)
		url = 'http://quotes.nasdaq.com/asp/SummaryQuote.asp?symbol=' + symbol
		req = urllib.request.urlopen(url)
		self.feed(req.read())

	def handle_starttag(self, tag, attrs):
		print('Encountered the beginning of a %s tag ' % tag)

	def handle_endtag(self, tag):
		print('Encountered the end of a %s tag ' % tag)

