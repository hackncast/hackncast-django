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

FRONTEND_TARGETS=$(shell grep "^gulp\.task" frontend/gulpfile.js | cut -d"'" -f2 | grep -v "^clean$$")

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
	$(MAKE) db_load

db_load:
	$(ON_VENV); ./manage.py social

bootstrap-dev: venv_clean venv_create venv_install
	$(RUN_ANSILBE) $(ANSIBLEOPTS) infra/ansible/postgresql.yml --tags install
	$(ON_VENV); ./manage.py migrate
	$(MAKE) db_load run

setup-env-vars:
	@echo -e $(BLUE)Updating env vars...$(NC)
	-rm $(ROOT_PATH)/settings/.env
	-cat infra/dev_env.sh > $(ROOT_PATH)/settings/.env

# Application targets
run: setup-env-vars
	@echo -e $(GREEN)Running Django...$(NC)
	$(ON_VENV); ./manage.py runserver_plus $(BIND)

browser:
	sleep 2
	xdg-open http://localhost:3000

run-n-watch:
	$(MAKE) -j3 browser run watch

clean:
	@echo -e $(RED)Cleaning python compiled files and folders...$(NC)
	find . -type d -name "__pycache__" | xargs -I% rm -rf %
	find . -type f -name "*.pyc" | xargs -I% rm -rf %

urls: setup-env-vars
	@echo -e $(GREEN)Listing project URLs...$(NC)
	@$(ON_VENV); ./manage.py show_urls

shell: setup-env-vars
	@echo -e $(GREEN)Running Django Shell...$(NC)
	$(ON_VENV); ./manage.py shell_plus

# Frontend targets
semantic:
	@echo -e $(BLUE)Building Semantic-UI...$(NC)
	cd frontend/; ./node_modules/gulp-cli/bin/gulp.js --gulpfile ./src/semantic/gulpfile.js build

$(FRONTEND_TARGETS):
	cd frontend/; ./node_modules/gulp-cli/bin/gulp.js $@

frontend:
	$(MAKE) -j3 semantic vendor img
	$(MAKE) -j2 css js

.PHONY: venv_clean venv_create venv_install db_clean db_load bootstrap-dev setup-env-vars run browser run-n-watch clean urls shell semantic frontend $(FRONTEND_TARGETS)
