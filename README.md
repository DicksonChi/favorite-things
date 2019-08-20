#  Favorite Things Coding Test
* [Dependencies](#dependencies)
* [Test Description and Approach](#test-description-and-approach)
* [Installation](#installation)
* [Running Locally](#running)
* [Testing](#testing)
* [Linting](#testing)
* [Deployment](#deployment)

## Dependencies

This project makes use of the tech stack and more:

* Python 3.6 - Programming language
* Django REST framework - REST API
* VueJs for the frontend development
* AWS LAMBDA and s3 bucket
* Zappa for deployment


## Test Description and Approach
This is a Single Page Application created with VueJs and consumes a REST API created with Django
to show the list of categories and the ranking of the favorite things under each categories.  

This solution can allow for usage by different users without using 
authentication but just a simple id that is saved on their browser once 
they enter the email they want to use.

* If the user has not used the application before it registers them with
that email. If they have used it before they continue with that email the
next time.

* There are default categories for every user in the system. 
    * Person
    * Place
    * Food  
* The user can add more categories if he wishes to and can also add, edit and delete
 favorites under those categories. 

* On the right side of the screen the users see the log of their actions 
performed by them on the application and the time they were performed. 

## Readme Notes

* If the command line starts with $, the command should run with user privileges
* If the command line starts with #, the command should run with root privileges

## Installation
* git clone git@github.com:DicksonChi/favorite-things.git
* `$ cd favorite_things`
* `$ virtualenv -p /usr/bin/python3 virtualenv`
* `$ source virtualenv/bin/activate`

##### TO INSTALL DEPENDENCIES FOR THE BACKEND
* `$ pip install -r py-requirements/dev.txt`

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

##### Backend Deployment
*  run this command

  ` $  ./scripts/get_ready_for_deployment.sh`

* Update the settings file in favorite_things/favorite_things and add zappa_django_utils in the list of apps

* cd to the path where the `manage.py` file is and then run 

`$ zappa init` 

* Provide default settings to your zappa_settings.json file:

```
- Name of environment - just accept the default 'dev'
- S3 bucket for deployments - just accept the default
- Zappa should automatically find the correct Django settings file so accept the default
```

* Go to your AWS console and create the VPC and then then the RDS and then update the zappa_settings.json file
```
    "vpc_config" : {
            "SubnetIds": [ "your-subnet-1", "your-subnet-2"],
            "SecurityGroupIds": ["your-security-group"]
        },
        "environment_variables": {
            "AWS_REGION": "YOUR_AWS_REGION",
            "AWS_SECRET_ACCESS_KEY": "YOUR AWS SECRET KEY IN YOUR .aws/credentials FILE",
            "AWS_ACCESS_KEY_ID": "YOUR AWS KEY ID IN YOUR .aws/credentials FILE",
            "SECRET_KEY": "YOUR_SECRET_KEY",
            "DATABASE_URL": "psql://USER:PASS@RDS_ENDPOINT:5432/DB_NAME"
        },
```
* Now run `$ zappa deploy <STAGE NAME>`
you should get this message 
```
Scheduled favorite-things-dev-zappa-keep-warm-handler.keep_warm_callback with expression rate(4 minutes)!
Deploying..
Your application is now live at https://URI.REGION.amazonaws.com/STAGE_NAME
```
* create a new bucket for the static folder and add this to your settings
```
STATIC_ROOT = os.path.join(BASE_DIR, "static")

AWS_S3_BUCKET_NAME_STATIC = "NEW_BUCKET_NAME"
AWS_S3_BUCKET_AUTH_STATIC = True
AWS_ACCESS_KEY_ID = "YOUR_KEY_ID"
AWS_SECRET_ACCESS_KEY = "YOUR SECRET KEY"
AWS_REGION = "YOUR REGION"
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_CUSTOM_DOMAIN = "{}.s3.amazonaws.com".format(AWS_S3_BUCKET_NAME_STATIC)
STATIC_URL = "https://{}/".format(AWS_S3_CUSTOM_DOMAIN)
```
* Then run the command to update this deployment
```
$ zappa update <stage_name>
```

* Now run this command to collect static for the admin view
```
$ python manage.py collectstatic --noinput
```

* Now lets create the db. Since we already have the VPC and the RDS setup
run this command
```
$ zappa manage <STAGE_NAME> create_pg_db
```

* If you get the error message that a db with same name exists, then ignore

* Now let us migrate, load fixtures and create admin user
```
$ zappa manage <STAGE_NAME> migrate
$ zappa invoke --raw dev "loaddata fixtures/default_category.json"
$ zappa invoke --raw dev "from main.models import User; User.objects.create_superuser(email='admin@ybritecore.com', password='password')"
```

##### Frontend Deployment
* After deploying the backend code get the endpoint URL and update the PROD constant in constants.js file in 
`frontend/src` 

* create the s3 bucket that will collect the static files for the frontend.

* Go to the bucket permission and then under the cors configuration copy this code to allow for public access
``` 
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
        <AllowedHeader>Authorization</AllowedHeader>
    </CORSRule>
    </CORSConfiguration>
```

* run this command to then deploy the frontend

* `$ cd frontend`

  `$  . ../scripts/build_frontend.sh  s3://NAME_OF_THE_BUCKET_YOU_CREATED`


* Copy the url of the static bucket and access it from your browser.
* Now you too can now make a list of your own favorite things!
