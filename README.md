# Software-Developer-Jobs-Cluster

This project is designed to scrape all the jobs on Reed that are "Software Developer" jobs in the UK. The aim was to see where the major clusters of jobs are around the UK. (Personally where to consider looking for jobs as an alternative to London...)

I am plan to expand the project to include other job boards and analyze furhter data about the job posts other than location.

#How the project was made
I used mainly Python and Sqlite3 for scraping and recording the information in a SQL database.

- createTables.py
  - Creates the tables needed in the Sqlite3 DB and can also delete the tables 
- geoReed.py
  - Retrieves the locations from DB and moves them to another table for the geolocation addresses
  - getGeoLocations.py method, retrieves the geolocations of the jobs according to the address scarpped from the Google Maps API.
    - The method filters locations outside of the UK's geolocation to remove any unwanted data.
    - geoDump.py then dumps the data into a JSON file
- updateLocations.py
  - Due to the limit of requests to the Google Maps API for geolocations, this program was created to scan the table for geoData.
  - It checks whether there is a matching address the already has the geoData retrieved.
  - It then updates the rows without geoData locations according to matched addresses.
  - This allows for only 2 calls to the Google Maps API for a data size of 4787 jobs
