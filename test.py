import httplib
conn = httplib.HTTPConnection('localhost', 8161)
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn.request('POST', '/demo/message/FOO/BAR', 'destination=foo&type=queue&body=hi', headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()
