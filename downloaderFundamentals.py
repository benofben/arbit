import google.downloader
import sched
import datetime
import time
import constants


class downloader:
    schedule = sched.scheduler(time.time, time.sleep)

    def __init__(self):
        # We don't want to run immediately because we won't get a close price
        today = datetime.date.today()

        downloadTime = constants.downloadtimeFundamentals
        downloadDateTime = datetime.datetime.combine(today, downloadTime)
        downloadTime = time.mktime(downloadDateTime.timetuple())

        print('Going to run fundamentals download next at ' + downloadDateTime.isoformat())
        self.schedule.enterabs(downloadTime, 0, self.download, ())
        self.schedule.run()

    def download(self):
        print('Running fundamentals download at ' + datetime.datetime.today().isoformat())
        google.downloader.run()
        print('Done with fundamentals download at ' + datetime.datetime.today().isoformat())

        # Reschedule the download to run again tomorrow.
        # Assume the system clock uses NY time.
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        downloadTime = constants.downloadtimeFundamentals
        downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
        downloadTime = time.mktime(downloadDateTime.timetuple())

        print('Going to run fundamentals download next at ' + downloadDateTime.isoformat())
        self.schedule.enterabs(downloadTime, 0, self.download, ())


downloader()
