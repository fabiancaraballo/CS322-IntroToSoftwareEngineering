# Project 7: Adding authentication and user interface to brevet time calculator service

Author: Fabian Caraballo
Email: fpc@uoregon.edu  


This is a project that extends proj6-rest.

In this project, we are adding authentication and user interface to the Brevet Time calculator service.

Part 1 of this project was getting the authentication work.

So to run part 1 properly.

- 1. Add data into the brevet calculator 
 - You can do this by "localhost:5000/"


- 2. POST /api/register
    - Unforntunately, I had this working and after adding CSRF Protection. However, you can register via the client on "localhost:5000" once your account is made you can then use the commands below in the terminal to get to the following apis!



- 3. GET /api/token
    - Once you are registered you can now get a token by running the command:
        - "curl -u <Username>:<Password> -i -X GET http://127.0.0.1:5001/api/token"
    - Or if you are in the client you can get the token by running "http://127.0.0.1:5001/api/token"

- 4. GET /RESOURCE-YOU-CREATED-IN-PROJECT-6
    - Copy the token from the /api/token and now you can get all the times which every way you can in the client by running any of the following commands with the token:
        -"http://<host:5001>/listAll" should return all open and close times in the database
            -"http://<host:5001>/listOpenOnly?token=<tokenValue>" should return open times only
            -"http://<host:5001>/listCloseOnly?token=<tokenValue>" should return close times only
            -"http://<host:5001>/listAll/csv?token=<tokenValue>" should return all open and close times in CSV format
            -"http://<host:5001>/listOpenOnly/csv?token=<tokenValue>" should return open times only in CSV format
            -"http://<host:5001>/listCloseOnly/csv?token=<tokenValue>" should return close times only in CSV format
            -"http://<host:5001>/listAll/json?token=<tokenValue>" should return all open and close times in JSON format
            -"http://<host:5001>/listOpenOnly/json?token=<tokenValue>" should return open times only in JSON format
            -"http://<host:5001>/listCloseOnly/json?token=<tokenValue>" should return close times only in JSON format
            -"http://<host:5001>/listOpenOnly/csv?top=3?token=<tokenValue>" should return top 3 open times only (in ascending order) in CSV format
            -"http://<host:5001>/listOpenOnly/json?top=5?token=<tokenValue>" should return top 5 open times only (in ascending order) in JSON format
            -"http://<host:5001>/listCloseOnly/csv?top=6?token=<tokenValue>" should return top 5 close times only (in ascending order) in CSV format
            -"http://<host:5001>/listCloseOnly/json?top=4?token=<tokenValue>" should return top 4 close times only (in ascending order) in JSON format


Part 2. The User Interface
    -1. Add values into the brevet calculator
        - "http://127.0.0.1:5000/

    -2. Go to the main page. 
        - "http://127.0.0.1:5001/"
            - Login if you already a user.
            - If you don't have an account click sign up. Which will take you to the registration page.
            - Make an account, then return to the login in page. 
            - Now you can use your account information to login.
            - Here you can see the same information in Part1. Number #4.

