import sqlite3

conn = sqlite3.connect('SoftwareJobs.sqlite3');
cur = conn.cursor();

cur.execute('''SELECT DISTINCT address, geoData, checked
FROM reedGeoData WHERE geoData IS NULL AND checked IS NULL''')
nullGeoData = cur.fetchall()

cur.execute('''SELECT DISTINCT address, geoData, checked
FROM reedGeoData WHERE geoData IS NOT NULL AND checked IS NOT NULL''')
location = cur.fetchall()

for eachNull in nullGeoData:
    for eachLocation in location:
        if eachNull[0] == eachLocation[0]:
            cur.execute('''UPDATE reedGeoData SET geoData=?, checked=1 WHERE address=?;
            ''', (eachLocation[1], eachNull[0]))
            conn.commit()
