import datetime
import math
import urllib
import csv
from io import StringIO

 run(event, context):
    # Date should look like this: '2018-04-02'
    date = event['date']

    # Compose the URL of the master file
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = datetime.date(date.year, date.month, date.day)
    year = str(date.year)
    quarter = 'QTR' + str(1 + math.ceil(date.month / 4))
    date = date.strftime('%Y%m%d')
    url = 'https://www.sec.gov/Archives/edgar/daily-index/'+ year + '/' + quarter + '/master.' + date + '.idx'

    # Download the master file
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')

    # Parse the master file and get filenames for Form 4
    form4URLs=[]
    f = StringIO(text)
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        if len(row) != 5:
            # Then this is a header row
            pass
        elif row[2] == '4':
            # This is a Form 4
            form4URLs.append('https://www.sec.gov/Archives/' + row[4])

    # Download and parse each Form 4
    for url in form4URLs:
        response = urllib.request.urlopen(url)
        data = response.read()
        text = data.decode('utf-8')


    return 1
