import briefing.sql as sql
import briefing.upgrades
import datetime
import constants

mySql = sql.sql()
#mySql.drop_table()
#mySql.create_table()

currentDate = constants.endDate
while currentDate>=constants.startDate:
    print('Downloading analyst upgrades for ' + currentDate.isoformat())
    briefing.upgrades.getUpgradesForDate(currentDate, mySql)
    currentDate = currentDate - datetime.timedelta(days=1)
