import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import edgar.sql
import google.sql
import yahoo.sql
import datetime

def run():
	currentDate = datetime.date.today() - datetime.timedelta(days=1)
	s = constructInsiderTable(currentDate)
	print('I am going to email a summary of inside trades for ' + currentDate.isoformat() + '.')
	mail(currentDate, s)
	
def constructInsiderTable(currentDate):
	edgarSql = edgar.sql.sql()
	forms = edgarSql.fetch(currentDate)

	googleSql = google.sql.sql()
	yahooSql = yahoo.sql.sql() 
		
	if not forms:
		return 'No insider trades today.'

	s = '<tr><td>' + 'Acceptance Datetime' + '</td><td>' + 'Transaction Date' + '</td><td>' + 'Symbol' + '</td><td>' + 'Insider Trade Price' + '</td><td>' + 'Close Price' + '</td><td>' + 'PE' + '</td><td>' + 'Yield' + '</td><td>' + 'Insider Name' + '</td><td>' + 'Insider Trade Shares' + '</td><td>' + 'Trade Value' + '</td><td>' + 'Shares Owned'+ '</td><td>' + 'Total Value'
	s+= '</td><td>' + 'Director' + '</td><td>' + 'Officer' + '</td><td>' + '10% Owner' + '</td><td>' + 'Other'
	s += '</td></tr>'
	
	for form in forms:
		symbol = form['IssuerTradingSymbol']
		fundamentals = googleSql.fetch(currentDate, symbol)
		quote = yahooSql.fetchForSymbolAndDate(symbol, currentDate)
		
		if fundamentals and quote:
			pe = calculatePE(fundamentals, quote)
			if pe > 0 and pe < 15 and marketPrice(form, yahooSql):
				tradeValue = form['TransactionPricePerShare'] * form['TransactionShares'] 
				totalValue = form['TransactionPricePerShare'] * form['SharesOwned'] #maybe use close price for this instead?  not sure...

				# assuming a quarterly dividend (this could be wrong!)
				stockYield = str(round((fundamentals['Dividend']/quote['Close'])*100*4,2))+'%'
				
				symbolString = '<a href="http://www.google.com/finance?q=' + symbol + '">' + symbol +'</a>'
				s+='<tr><td>' + str(form['AcceptanceDatetime']) + '</td><td>' + str(form['TransactionDate'].strftime('%Y-%m-%d')) + '</td><td>' + symbolString + '</td><td>' + '$' + str(round(form['TransactionPricePerShare'],2)) + '</td><td>' + '$' + str(round(quote['Close'],2)) + '</td><td>' + str(round(pe,2)) + '</td><td>' + stockYield + '</td><td>' + form['RptOwnerName'] + '</td><td>' + str(int(form['TransactionShares'])) + '</td><td>' + '$' + str(round(tradeValue,2)) + '</td><td>' + str(int(form['SharesOwned'])) + '</td><td>' + '$' + str(round(totalValue,2))
				s+= '</td><td>' + form['IsDirector'] + '</td><td>' + form['IsOfficer'] + '</td><td>' + form['IsTenPercentOwner'] + '</td><td>' + form['IsOther']
				s+='</td></tr>'	
	
	if len(s)==326:
		# Then no trades matched above
		return 'None of the ' + str(len(forms)) + ' insider trades on ' + currentDate.isoformat() + ' met our criteria.'
	
	return s

def marketPrice(form, yahooSql):
	#returns true if low<price<high, otherwise false
	quote = yahooSql.fetchForSymbolAndDate(form['IssuerTradingSymbol'], form['TransactionDate'])
	
	if not quote:
		return False
	
	if quote['Low']<=form['TransactionPricePerShare'] and quote['High']>=form['TransactionPricePerShare']:
		return True
	
	return False

def calculatePE(fundamentals, quote):
	if fundamentals['EPS']==0:
		pe = 0
	else:
		pe = quote['Close']/fundamentals['EPS']
	return pe

def mail(currentDate, s):	
	fromAddress = 'ben.lackey@hotmail.com'
	recipients = ['ben.lackey@hotmail.com']
	login    = fromAddress
	password = 'foobar123'
	
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Insider Trades for ' + currentDate.strftime('%Y-%m-%d')
	msg['From'] = fromAddress
	msg['To'] = ", ".join(recipients)
	
	# Create the body of the message (a plain-text and an HTML version).
	text = 'This email can only be viewed as HTML.'
	html = '<html><head></head><body><table border="1" cellpadding="5">' + s + '</table></body></html>'
	
	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	
	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	server = smtplib.SMTP('smtp.live.com', 587)
	#server.set_debuglevel(1)
	server.ehlo()
	server.starttls()
	server.login(login, password)
	server.sendmail(fromAddress, recipients, msg.as_string())
	
	server.quit()