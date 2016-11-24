import urllib
import sqlite3
import json
import time
import ssl
import codecs
import unittest

class LocationTable():
    def __init__(self):
        self.conn = sqlite3.connect('SoftwareJobs.sqlite3');
        self.cur = self.conn.cursor();

    def locationGeoData(self):
        self.cur.execute('''SELECT COUNT (location) AS locationCount FROM Reed ''')
        self.locationCount = self.cur.fetchone()
        self.locationCount = int(self.locationCount[0])
        self.count = 1
        try:
            while self.locationCount > 0:
                self.cur.execute('''SELECT id, location FROM Reed WHERE id=?''', (self.count,));
                self.row = self.cur.fetchone()
                self.rowId = self.row[0]
                self.address = str(self.row[1] + " Europe ")

                print type(self.address)
                print self.rowId, self.address

                self.count += 1
                self.cur.execute(''' INSERT INTO reedGeoData (reed_id, address) VALUES (?,?); ''', (self.rowId, self.address,))

                self.locationCount -= 1

                if self.locationCount < 1:
                    self.conn.commit()

        except Exception, e:
            print "No more left to scrape"

    def getGeoLocations(self):
        self.serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"

        self.scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.scontext = None
        self.test = 1
        self.apiCount = 0

        while True:
            self.cur.execute(''' SELECT reed_id, address, geoData, checked FROM reedGeoData WHERE checked IS NULL ORDER BY RANDOM() LIMIT 1''')
            self.row = self.cur.fetchone()
            self.reedId = self.row[0]
            self.address = self.row[1]
            self.geoData = self.row[2]
            self.checked = self.row[3]

            self.url = self.serviceurl + urllib.urlencode({"sensor":"false", "address": self.address})
            # print 'Retrieving', self.url
            self.uh = urllib.urlopen(self.url, context=self.scontext)

            # #data == uh.read() read the the data from uh
            self.data = self.uh.read()
            # print 'Retrieved',len(self.data),'characters',self.data[:20].replace('\n',' ')
            # print "This is the datatype: ",type(self.data)

            try:
                # pretty print the data?
                self.js = json.loads(str(self.data))
                print self.js
                # print "This is the pretty print: ",self.js  # We print in case unicode causes an error
                self.lat = self.js["results"][0]["geometry"]["location"]["lat"]
                self.lng = self.js["results"][0]["geometry"]["location"]["lng"]
                print "This is the lat", self.lat
                print "This is the lng", self.lng
                if self.lat > 59.7 or self.lat < 50.4: continue
                if self.lng < -4 or self.lng > 1.9: continue

            except:
                continue

            self.apiCount += 1

            if self.apiCount % 10 == 0:
                time.sleep(5)

            if 'status' not in self.js or (self.js['status'] != 'OK' and self.js['status'] != 'ZERO_RESULTS') :
                print '==== Failure To Retrieve ===='
                print self.data
                break

            self.cur.execute(''' UPDATE reedGeoData SET checked=?, geoData=? WHERE reed_id=?; ''', (1, buffer(self.data), self.reedId,))
            self.conn.commit()

    def geoDump(self):
        self.cur.execute(''' SELECT reed_id, address, geoData FROM reedGeoData WHERE checked IS NOT NULL''')
        self.fhand = codecs.open('jobLocations.js', 'w', "utf-8")
        self.clusterData = codecs.open('Job Clustering/dataLocations.js', 'w', 'utf-8')
        # #
        self.fhand.write("myData = [\n")
        self.clusterData.write("[\n")

        self.count = 0

        for self.row in self.cur:
            self.data = str(self.row[2])
            # print self.data
            self.count += 1
            # print self.count
            try:
                self.js = json.loads(str(self.data))
                # print self.js
            except Exception, e: print str(e)

            if not('status' in self.js and self.js['status'] == 'OK') : continue

            self.lat = self.js["results"][0]["geometry"]["location"]["lat"]
            self.lng = self.js["results"][0]["geometry"]["location"]["lng"]
            self.locationData = self.js["results"][0]["address_components"][-1]["short_name"]

            if self.lat == 0 or self.lng == 0 : continue
            if self.locationData != "GB": continue
            self.where = self.js['results'][0]['formatted_address']
            self.where = self.where.replace("'","")

            try :
                # print self.where, self.lat, self.lng

                self.count += 1
                if self.count > 1 : self.fhand.write(",\n")
                if self.count > 1 : self.clusterData.write(", \n")
                #writing each list/line to the .js file

                self.clusterOutput = "{" + "lat: " + str(self.lat) + ", " + "lng: " + str(self.lng) + "}"
                self.output = "["+str(self.lat)+","+str(self.lng)+", '"+self.where+"']"
                self.clusterData.write(self.clusterOutput)
                self.fhand.write(self.output)
            except:
                continue

        #write a new line after each line?
        self.fhand.write("\n];\n")
        self.clusterData.write("\n];\n")
        #close the cursor
        self.cur.close()
        #close the fhand to finalize what has been written into the file
        self.fhand.close()
        self.clusterData.close()

class ProgramRoot():
    def __init__(self):
        self.introMessage = raw_input("\n*******************README*********************\n\nIn this program, to select 'yes' press <enter> / to select 'no' type 'n' at the prompt\nContinue?.... ")
        if len(self.introMessage) < 1 :
            self.connectDB = raw_input("Connect to the SoftwareJobs.sqlite3 database?: ")
            if len(self.connectDB) < 1:
                self.table = LocationTable()
                self.chooseTable()

    def chooseTable(self):

        while True:
            self.chooseMethod = raw_input("Enter the corresponding number to the action\n\n1: Move locations from Reed to reedGeoTable\n\n2: Retrieve GeoLocations from Google Maps\n\n3: Dump geoData to JSON\n\nTo Exit Program: n\n\nEnter table number: ")

            if self.chooseMethod == "1":
                self.table.locationGeoData()
                print "Migrating Locations from Reed to reedGeoData Table..."

            if self.chooseMethod == "2":
                self.table.getGeoLocations()
                print "Retrieved GeoLocations from Google Maps API..."

            if self.chooseMethod == "3":
                try:
                    self.table.geoDump()
                    print "Dumping geoData locations to json"
                except:
                    print "No more data left to dump"

            if self.chooseMethod == 'n':
                print "Exiting Program"
                break

initialize = ProgramRoot()
