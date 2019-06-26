# Project 5: Brevet time calculator with Ajax and MongoDB

Simple list of controle times from project 4 stored in MongoDB database.

Author: Fabian Caraballo, Ram Durairajan for acp_times.py
Email: fpc@uoregon.edu
(https://bitbucket.org/fabiancaraballo/proj4-brevets/) for most of the code, added some other files to this project.



We are building off of proj4-brevets, this project consists of using mongoDB as well as docker-compose
to help store items into a Mongo database. We use the ACP time calculator to help the user find out how long it will take for each ACP brevet control based off of time and distance. 

The user inputs how long far they will be riding, the date, and time. Then in the table they can input how long it would take for them to ride each interval in either miles or Kilometers then the calculator will automatically calculate how long it will take from opening time to closing time.

If they press the submit button it will get sent into a database where it will record their time intervals then if they press display it will take them to a page where it will show the checkpoints, opening times and closing times.

Some of the rules to make sure you implement in the calculator to ensure the best calculation possible:
    - Make sure the date ranges from the year 2000-2018
    - Make sure when you start the calculator it starts at 0 becuase that represents the starting location of you brevet.
    - Make sure the KM portion of the table doesn't go over the distance you choose in the 200 km, 400 km, 600 km, 800 km, or 1000 km.
    