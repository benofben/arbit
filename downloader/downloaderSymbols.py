import sched
import datetime
import time
import constants
import nasdaq.downloader


class downloader:
    schedule = sched.scheduler(time.time, time.sleep)


    def __init__(self):
        self.schedule.enterabs(time.time(), 0, self.download, ())
        self.schedule.run()


    def download(self):
        print('Running symbols download at ' + datetime.datetime.today().isoformat())
        nasdaq.downloader.run()
        print('Done with symbols download at ' + datetime.datetime.today().isoformat())

        # Reschedule the download to run again tomorrow.
        # Assume the system clock uses NY time.
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        downloadTime = constants.downloadtimeSymbols
        downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
        downloadTime = time.mktime(downloadDateTime.timetuple())

        print('Going to run symbols download next at ' + downloadDateTime.isoformat())
        self.schedule.enterabs(downloadTime, 0, self.download, ())


downloader()
