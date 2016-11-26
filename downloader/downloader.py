import sys
import sched
import datetime
import time
import constants

class downloader:
    schedule = sched.scheduler(time.time, time.sleep)


    def __init__(self, type):
        # going to need to add some code to delay for fundamentals

        self.schedule.enterabs(time.time(), 0, self.download, (type,))
        self.schedule.run()


    def download(self, type):
        print('Running download at ' + datetime.datetime.today().isoformat())

        if type == 'symbols':
            import symbols
            symbols.run()
        else type == 'quotes':
            import quotes
            quotes.run()
        else type == 'fundamentals':
            import fundamentals
            fundamentals.run()
        else type == 'edgar':
            import edgar
            edgar.downloader.run()

        print('Done with download at ' + datetime.datetime.today().isoformat())

        # Reschedule the download to run again tomorrow.
        # Assume the system clock uses NY time.
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        downloadTime = constants.downloadtime[type]
        downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
        downloadTime = time.mktime(downloadDateTime.timetuple())

        print('Going to run download next at ' + downloadDateTime.isoformat())
        self.schedule.enterabs(downloadTime, 0, self.download, ())


def main(argv):
    if(len(argv) != 2):
        print('Wrong number of arguments: ' + str(len(argv)))
        print('Usage: python3 downloader.py [symbols|quotes|fundamentals|edgar]')
        exit(1)

    types = ['symbols', 'quotes', 'fundamentals', 'edgar']
    type = sys.argv[1]
    if not type in types:
        print('Invalid argument: ' + type)
        print('Usage: python3 downloader.py [symbols|quotes|fundamentals|edgar]')
        exit(1)

    print('Creating a downloader of type ' + type)
    downloader(type)


if __name__ == "__main__":
   main(sys.argv)
