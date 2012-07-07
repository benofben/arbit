import cx_Oracle
import sys

class sql():
    def __init__(self):
        self.connection = cx_Oracle.connect('arbit/arbit@orcl')        
        
    def create_table(self):    
        cursor = self.connection.cursor()
        sql = 'CREATE TABLE AnalystUpgrades(RatingsChangeDate date, Company varchar(39), Ticker varchar(8), BrokerageFirm varchar(26), RatingsChange varchar(35), PriceTarget varchar(35), CONSTRAINT AnalystUpgradesPK PRIMARY KEY (RatingsChangeDate, Ticker, BrokerageFirm))'
        
        try:    
            response = cursor.execute(sql)
            print(response)
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print(sys.stderr, "Oracle-Error-Code:", error.code)
            print(sys.stderr, "Oracle-Error-Message:", error.message)
        self.connection.commit()
        cursor.close()
        
    def drop_table(self):
        cursor = self.connection.cursor()
        sql = 'DROP TABLE AnalystUpgrades'
        try:    
            response = cursor.execute(sql)
            print(response)
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print(sys.stderr, "Oracle-Error-Code:", error.code)
            print(sys.stderr, "Oracle-Error-Message:", error.message)
        self.connection.commit()
        cursor.close()
        
    def __del__(self):
        self.connection.close()

    def insert(self, upgrade):    
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO AnalystUpgrades(RatingsChangeDate, Company, Ticker, BrokerageFirm, RatingsChange, PriceTarget) VALUES (:RatingsChangeDate, :Company, :Ticker, :BrokerageFirm, :RatingsChange, :PriceTarget)",
            {
                'RatingsChangeDate' : upgrade['RatingsChangeDate'],
                'Company' : upgrade['Company'],
                'Ticker' : upgrade['Ticker'],
                'BrokerageFirm' : upgrade['BrokerageFirm'],
                'RatingsChange' : upgrade['RatingsChange'],
                'PriceTarget' : upgrade['PriceTarget'],
            }
        )
        self.connection.commit()
        cursor.close()
        
    def fetch(self, currentDate):
        cursor = self.connection.cursor()
        
        cursor.execute("SELECT RatingsChangeDate, Company, Ticker, BrokerageFirm, RatingsChange, PriceTarget FROM AnalystUpgrades WHERE RatingsChangeDate=:CurrentDate",
            CurrentDate = currentDate
        )
        
        rows = cursor.fetchall()
        if not rows:
            return None
        
        upgrades = []        
        for row in rows:
            upgrade = {}
            upgrade['RatingsChangeDate']=row[0]
            upgrade['Company']=row[1]
            upgrade['Ticker']=row[2]
            upgrade['BrokerageFirm']=row[3]
            upgrade['RatingsChange']=row[4]
            upgrade['PriceTarget']=row[5]
            upgrades.append(upgrade)
        cursor.close()
        
        return upgrades
