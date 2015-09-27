import yahoo.database

quoteDB = yahoo.database.database()
quotes = quoteDB.writeQuotesToDisk()
