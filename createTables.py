import sqlite3

class SQLTables():
    def __init__(self):
        self.conn = sqlite3.connect('SoftwareJobs.sqlite3', timeout=10);
        self.cur = self.conn.cursor();

    def reedTable(self):
        try:
            self.cur.execute(''' DROP TABLE IF EXISTS Reed; ''')
            self.cur.execute('''
            CREATE TABLE Reed (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, title TEXT, location TEXT, geoData TEXT,
            salary TEXT, jobType TEXT, applicants INTEGER, recruiter TEXT)
            ''')
            self.conn.commit();

        except Exception, e:
            print str(e);


    def reedGeoData(self):
        try:
            self.cur.execute(''' DROP TABLE IF EXISTS reedGeoData; ''')
            self.cur.execute('''
            CREATE TABLE reedGeoData (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, reed_id INTEGER UNIQUE, address TEXT, geoData TEXT, checked INTEGER)''')
            self.conn.commit();

        except Exception, e:
            print str(e);


class ProgramRoot():
    def __init__(self):
        self.introMessage = raw_input("\n*******************README*********************\n\nIn this program, to select 'yes' press <enter> / to select 'no' type 'n' at the prompt\nContinue?.... ")
        if len(self.introMessage) < 1 :
            self.connectDB = raw_input("Connect to the SoftwareJobs.sqlite3 database?: ")

            if len(self.connectDB) < 1:
                self.table = SQLTables()
                self.chooseTable()

    def chooseTable(self):

        while True:
            self.createTable = raw_input("Enter the corresponding number to create/reset the tables\n\n1: Reed\n2: Reed Geo Data Table\n\nTo Exit Program: n\n\nEnter table number: ")
            if self.createTable == "1":
                try:
                    print "Creating/Resetting the Reed Table...."
                    self.table.reedTable()
                except Exception, e:
                    print str(e)

            if self.createTable == "2":
                print "Creating/Resetting the Geo Data Reed Table...."
                self.table.reedGeoData()

            if self.createTable == 'n':
                print "Exiting Program"
                break


initialize = ProgramRoot()
