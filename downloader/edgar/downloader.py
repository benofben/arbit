import sched
import datetime
import time
import main


class downloader:
    schedule = sched.scheduler(time.time, time.sleep)

    def __init__(self):
        # It looks like new master files show up at 2:01am, though are sometimes delayed as late as 2:14am.
        # Something else is showing up at 10pm eastern, but it's unclear from my old comments.  Need to investigate.
        downloadTime = datetime.time(22,30,0)
        today = datetime.date.today()
        downloadDateTime = datetime.datetime.combine(today, downloadTime)
        downloadTime = time.mktime(downloadDateTime.timetuple())

        print('Going to run EDGAR download next at ' + downloadDateTime.isoformat())
        self.schedule.enterabs(downloadTime, 0, self.download, ())
        self.schedule.run()

    def download(self):
        print('Running EDGAR download at ' + datetime.datetime.today().isoformat())
        edgar.downloader.run()
        #edgar.mail.run()
        print('Done with EDGAR download at ' + datetime.datetime.today().isoformat())

        # Reschedule the download to run again tomorrow.
        # Assume the system clock uses NY time.
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        downloadTime = constants.downloadtimeEDGAR
        downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
        downloadTime = time.mktime(downloadDateTime.timetuple())

        print('Going to run EDGAR download next at ' + downloadDateTime.isoformat())
        self.schedule.enterabs(downloadTime, 0, self.download, ())


downloader()
