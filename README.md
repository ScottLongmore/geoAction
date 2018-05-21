geoAction/polygonAction
======
:Description: Flask RESTful API that takes geoJSON POST containing two polygon features and finds either the intersection or union given by the route. Geojson files must contain a FeatureCollection with exactly two polygon features. See the the polygonPair.json example file.  
:Keywords: geojson, intersection, union, flask, shapely  
:Version:0.1.0  
:Last Edit: 2018-5-20  
:Author: Scott Longmore  
:Contact: Scott.Longmore@gmail.com  

**Syntax** 

To run the polyAction service, start the flask service: 

> python run.py &

For an example intersection of two geojson polygon pairs:

> curl -X POST -H "Content-Type: application/json" -d @example/polygonPair.json http://127.0.0.1:5000/polygonAction/intersection

For an example union of two geojson polygon pairs:

> curl -X POST -H "Content-Type: application/json" -d @example/polygonPair.json http://127.0.0.1:5000/polygonAction/union  

To run polygonAction tests in tests directory:

> python polygonAction_tests.py -v 

**Directory/File Structure** 

* run.py - runs polygonAction flask service
* config.py - configuration for polygonAction service
* requirements.txt - python module requirements
* geoAction/ - contains polygonAction app 
    * polygonAction.py - takes two polygon geojson features and returns either the intersection or union as specified in the route
* example/ - directory containing example geojson file
    * polygonPair.json - Colorado geojson polygon example 
* tests/ -  
    * polygonAction_tests.py - flask unit tests for polygonAction service
    * fixtures/ - test geojson data fixtures

