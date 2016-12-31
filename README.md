# Software-Developer-Jobs-Cluster

#How the project was made
Python and Sqlite3 were used for scraping and recording the information in a SQL database.

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
  
# Software Developer Job Cluster (UK)

This project was designed to represent software development jobs in the UK as a cluster via Google Maps API. The job posts were scraped from  www.reed.co.uk using "Software Developer" as the search query. The goal was to show the location of software development job clusters in the UK.

I am plan to expand the project to include other job boards and analyze further data about the job posts.

## Built With

* Python
* SQL
* HTML/CSS/JavaScript

## Authors

* [ChristopherCoverdale](https://github.com/ccdle12)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

