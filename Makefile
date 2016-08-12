RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

ANSIBLEOPTS=-K

BIND ?= localhost:8000
DEBUG ?= 0
ifeq ($(DEBUG), 1)
	ANSIBLEOPTS += -vv
endif

VENV_NAME=hackncast-django
ROOT_PATH=hnc
WORKON_HOME?=$(realpath $$WORKON_HOME)
ON_VENV=. $(WORKON_HOME)/$(VENV_NAME)/bin/activate
LOAD_VENV=. /usr/bin/virtualenvwrapper.sh
RUN_ANSILBE=. ./infra/dev_env.sh; ansible-playbook -i localhost, 

# Environment target
venv_clean:
	@echo -e $(BLUE)Removing venv...$(NC)
	$(LOAD_VENV); rmvirtualenv $(VENV_NAME)

venv_create:
	@echo -e $(BLUE)Creating venv...$(NC)
	$(LOAD_VENV); mkvirtualenv --python /usr/bin/python3 $(VENV_NAME)

venv_install:
	@echo -e $(BLUE)Installing requirements...$(NC)
	$(ON_VENV); pip install --upgrade pip
	$(ON_VENV); pip install -r requirements/development.txt

db_clean:
	$(RUN_ANSILBE) $(ANSIBLEOPTS) infra/ansible/postgresql.yml --tags clean
	$(ON_VENV); ./manage.py migrate

bootstrap-dev: venv_clean venv_create venv_install
	$(RUN_ANSILBE) $(ANSIBLEOPTS) infra/ansible/postgresql.yml --tags install
	$(ON_VENV); ./manage.py migrate
	$(MAKE) run

setup-env-vars:
	@echo -e $(BLUE)Updating env vars...$(NC)
	-rm $(ROOT_PATH)/settings/.env
	-cat infra/dev_env.sh > $(ROOT_PATH)/settings/.env
	@echo -e $(GREEN)Done!$(HN)

# Application targets
run: setup-env-vars
	@echo -e $(GREEN)Running Django...$(NC)
	$(ON_VENV); ./manage.py runserver_plus $(BIND)

clean:
	@echo -e $(RED)Cleaning python compiled files and folders...$(NC)
	find . -type d -name "__pycache__" | xargs -I% rm -rf %
	find . -type f -name "*.pyc" | xargs -I% rm -rf %
	@echo -e $(GREEN)Done!$(HN)

urls: setup-env-vars
	@echo -e $(GREEN)Listing project URLs...$(NC)
	@$(ON_VENV); ./manage.py show_urls

shell: setup-env-vars
	@echo -e $(GREEN)Running Django Shell...$(NC)
	$(ON_VENV); ./manage.py shell_plus

# Frontend targets
frontend-semantic:
	@echo -e $(BLUE)Building Semantic-UI...$(NC)
	cd frontend/; ./node_modules/gulp-cli/bin/gulp.js --gulpfile ./semantic/gulpfile.js build
	@echo -e $(GREEN)Done!$(HN)

frontend-clean:
	@echo -e $(RED)Cleaning frontend files and folders...$(NC)
	rm -rf frontend/static/*
	@echo -e $(GREEN)Done!$(HN)

.PHONY: clean
