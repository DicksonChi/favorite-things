# InvoizPaid Dashboard

## Readme Notes

* If the command line starts with $, the command should run with user privileges
* If the command line starts with #, the command should run with root privileges


## Retrieve code

* `$ git clone https://richardoyudo@gitlab.int.seedstars.com/invoizpaid/dashboard.git`
* `$ cd dashboard`
* `$ git submodule add https://github.com/Seedstars/culture-scripts scripts`
* `$ git submodule init`
* `$ git submodule update`
* `$ ./scripts/get_static_validation.sh`


## Installation

* Install [Weasy Print Dependencies] for your platform
* Install `qpdf` and `pdftohtml` dependencies for your platform

* `$ virtualenv -p /usr/bin/python3 virtualenv`
* `$ source virtualenv/bin/activate`
* `$ pip install -r py-requirements/dev.txt`

* `$ cd src`
* `$ python manage.py migrate`
* `$ python manage.py runserver`

## Running

* `$ cd src`
* `$ python manage.py runserver`

## Testing

* `$ ./scripts/test_local_backend.sh`


### Static analysis

* `$ ./scripts/static_validate_backend.sh`

[Weasy Print Dependencies]: http://weasyprint.readthedocs.io/en/stable/install.html
