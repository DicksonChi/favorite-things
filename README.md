# My Favorite Things Test

## Test Description and Approach
This is a Single Page Application created with VueJs and consumes a REST API created with Django
to show the list of categories and the ranking of the favorite things under each categories  

This solution can allow for usage by different users without using 
authentication but just a simple id that is saved on their browser once 
they type in the email they want to use.

* If the user has not used the application before it registers them with
that email. If they have used it before they continue with that email the
next time.

* There are defaults categories for every user in the system. 
    * Person
    * Place
    * Food  
* The user can add more categories if he wishes to and can also add, edit and delete
 favorites under those categories. 

* On the right side of the screen the users see the log of their actions 
performed by them on the application and the time they were performed 

## Readme Notes

* If the command line starts with $, the command should run with user privileges
* If the command line starts with #, the command should run with root privileges

## Installation
* `$ virtualenv -p /usr/bin/python3 virtualenv`
* `$ source virtualenv/bin/activate`

##### TO INSTALL DEPENDENCIES FOR THE BACKEND
* `$ pip install -r py-requirements/local.txt`

##### TO INSTALL DEPENDENCIES FOR THE FRONTEND
* `$ cd frontend`
* `$ npm install`

## Running

##### TO RUN BACKEND
* `$ cd favorite_things `
* `$ python manage.py migrate`
* `$ python manage.py runserver`


##### TO RUN FRONTEND
* `$ cd frontend `
* `$ npm run serve`


## Testing

##### Test backend
* `$ ./scripts/test_local_backend.sh`
* This scripts runs the `pytest` command and then creates coverage report when run. 

##### Test frontend
* `$ ./scripts/test_local_frontend.sh`
* This scripts runs the `npm run coverage` command.

##### cleanup after testing
* `$ ./scripts/cleanup.sh`
* after running the test there might be `.pyc ` or `__pycache__` files
so this script runs through all directories and cleans up.


## Linting
##### Linting and static analysis backend
* `$ ./scripts/static_validate_backend.sh`
* This script checks for the PEP issues with the python code and uses 
the `prospector.yml` defined conditions and using pylint to also check 
for linting issues in the python code and alerts you to conform to the standard.

##### Linting and static analysis frontend
* `$ ./scripts/static_validate_backend.sh`

* The script runs the `npm run lint` command to apply linting
and fixes to your Vue.js code


## Deployment

* 


