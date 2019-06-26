# Project 6: Brevet time calculator service

Author: Fabian Caraballo
Email: fpc@uoregon.edu

proj6-rest

This project builds off of proj5-mongo using restAPI

This project uses the same calculator from proj5 and stores it into a mongoDB 

To launch this app: 
use port 5000

To reach the consumer program:
use port 5002

To reach the basic API's:
use port 5001

-"http://<host:5001>/listAll" should return all open and close times in the database
-"http://<host:5001>/listOpenOnly" should return open times only
-"http://<host:5001>/listCloseOnly" should return close times only
-"http://<host:5001>/listAll/csv" should return all open and close times in CSV format
-"http://<host:5001>/listOpenOnly/csv" should return open times only in CSV format
-"http://<host:5001>/listCloseOnly/csv" should return close times only in CSV format
-"http://<host:5001>/listAll/json" should return all open and close times in JSON format
-"http://<host:5001>/listOpenOnly/json" should return open times only in JSON format
-"http://<host:5001>/listCloseOnly/json" should return close times only in JSON format
-"http://<host:5001>/listOpenOnly/csv?top=3" should return top 3 open times only (in ascending order) in CSV format
-"http://<host:5001>/listOpenOnly/json?top=5" should return top 5 open times only (in ascending order) in JSON format
-"http://<host:5001>/listCloseOnly/csv?top=6" should return top 5 close times only (in ascending order) in CSV format
-"http://<host:5001>/listCloseOnly/json?top=4" should return top 4 close times only (in ascending order) in JSON format
