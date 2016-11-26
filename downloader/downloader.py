import sched
import datetime
import time


class downloader:
    dataDirectory='/home/benton_lackey/arbit_data/'

    downloadtime = {
        'symbols':datetime.time(0,10,0),
        'quotes':datetime.time(0,30,0),
        'fundamentals':datetime.time(16,30,0),
        'edgar':datetime.time(22,30,0)
    }

    schedule = sched.scheduler(time.time, time.sleep)


    def __init__(self):
        self.schedule.enterabs(time.time(), 0, self.download, ())
        self.schedule.run()


    def download(self):
        print('Running download at ' + datetime.datetime.today().isoformat())
        symbols.downloader.run()
        print('Done with download at ' + datetime.datetime.today().isoformat())

        # Reschedule the download to run again tomorrow.
        # Assume the system clock uses NY time.
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        downloadTime = constants.downloadtimeSymbols
        downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
        downloadTime = time.mktime(downloadDateTime.timetuple())

        print('Going to run download next at ' + downloadDateTime.isoformat())
        self.schedule.enterabs(downloadTime, 0, self.download, ())


downloader()
