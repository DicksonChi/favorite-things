#!/usr/bin/env bash

pip install -r py-requirements/production.txt
pip install zappa # install the latest zappa
pip install zappa-django-utils # install to manage the lamda environment.