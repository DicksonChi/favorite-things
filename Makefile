.PHONY: requirements

# Set environment variables
ENVIRONMENT = set -o allexport; . ./.env; set +o allexport;

# Set the following variable to you project name
PROJECT_NAME = favorite_things
FRONT_END = frontend
DEFAULT_VIRTUALENV = .venv
# Possible virtualenv if virtualenvwrapper is used
POSSIBLE_VIRTUALENV = $(VIRTUAL_ENV)
# Use possible virtualenv if it exists and virtualenvwrapper is used, otherwise use default one
VIRTUALENV = $(if $(wildcard $(POSSIBLE_VIRTUALENV)),$(POSSIBLE_VIRTUALENV),$(DEFAULT_VIRTUALENV))

PYVERSION=3.6
PIP = $(VIRTUALENV)/bin/pip
PYTHON = $(VIRTUALENV)/bin/python
PYTEST = $(VIRTUALENV)/bin/pytest

app=
apps=

venv:
	@echo "Creating virtual environment within \"$(VIRTUALENV)\" directory"
	@python$(PYVERSION) -m venv $(VIRTUALENV) || rm -rf $(VIRTUALENV) && virtualenv -p `which python$(PYVERSION)` $(VIRTUALENV)

environment:
	@echo "python version"
	@echo "$(PYVERSION)"

requirements_dev:
	@echo "Installing $(PROJECT_NAME) requirements dev"
	@$(PIP) install -r py-requirements/dev.txt

requirements_prod:
	@echo "Installing $(PROJECT_NAME) requirements production"
	@$(PIP) install -r py-requirements/production.txt

collectstatic:
	@echo "Collecting static files for Django site"
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py collectstatic --noinput

run:
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py runserver

migrations:
	@echo "Generating migrations"
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py makemigrations $(apps)

migrate:
	@echo "Applying migrations"
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py migrate -v 0 --noinput $(app)

superuser:
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py createsuperuser

clean:
	@echo "Cleaning __pycache__ directories, .pyc and other unwanted files..."
	. scripts/cleanup.sh

lint_backend:
	@echo "Checking lint issues"
	. scripts/static_validate_backend.sh

lint_frontend:
	@echo "Checking lint issues"
	. scripts/static_validate_frontend.sh

test:
	@echo "Running test..."
	. scripts/test_local_backend.sh

install-fd:
	@echo "Start to install frontend dependencies..."
	@cd $(FRONT_END)/ && npm install

serve:
	@echo "Start serving frontend..."
	@cd $(FRONT_END)/ && npm run serve


build_deploy:
	@echo "Start building frontend..."
	@cd $(FRONT_END) && npm install && npm run build
	@cd $(FRONT_END) && aws s3 cp dist/ $(bucket) --recursive
	@echo "Your have successfully deployed the frontend now go and copy the Url from the bucket end point and enjoy!"

backend_deploy_start:
	@echo "Get the backend ready for deployment.."
	. scripts/get_ready_for_deployment.sh
	@cd $(PROJECT_NAME) && zappa init

backend_deploy:
	@echo "Deploying backend for $(stage).."
	@cd $(PROJECT_NAME) && zappa deploy $(stage)

backend_update:
	@echo "Updating backend for $(stage).."
	@cd $(PROJECT_NAME) && zappa update $(stage)

backend_create_db:
	@echo "Creating DB for $(stage).."
	@cd $(PROJECT_NAME) && zappa manage $(stage) create_pg_db

backend_migrate:
	@echo "Migrate db backend for $(stage).."
	@cd $(PROJECT_NAME) && zappa manage $(stage) migrate

backend_command:
	@echo "Execute $(command) backend.."
	@cd $(PROJECT_NAME) && zappa invoke --raw dev $(command)

