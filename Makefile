PYTHON = python3
PIP = $(PYTHON) -m pip
.PHONY: deps-update deps-init pre-commit requirements init clean report build release-test release-prod help

# Default target executed when no arguments are given to make.
all: help

pre-commit:
	pre-commit install && \
	pre-commit autoupdate && \
	pre-commit run --all-files

# pip-compile requirements/common.in && \
# pip-compile requirements/local.in && \
# $(PIP) install -r requirements/common.txt && \

requirements:
	rm -rf .tox && \
	$(PIP) install --upgrade pip wheel && \
	$(PIP) install -r requirements/local.in && \
	npm install && \

init:
	rm -rf venv .pytest_cache __pycache__ .pytest_cache node_modules && \
	python3.11 -m venv venv && \
	. venv/bin/activate && \
	make requirements

clean:
	rm -rf build dist secure_logger.egg-info

report:
	cloc . --exclude-ext=svg,json,zip --vcs=git

#######################################
# Django dev setup
#######################################
dev-db:
	mysql -uroot -p < memberpress_client/scripts/init-db.sql

dev-up:
	brew services start mysql
	brew services start redis

dev-down:
	brew services stop mysql
	brew services stop redis

django-server:
	./manage.py runserver 0.0.0.0:8000

django-migrate:
	./manage.py migrate
	./manage.py makemigrations memberpress_client
	./manage.py migrate memberpress_client

django-shell:
	./manage.py shell_plus


django-quickstart:
	make requirements
	make dev-up
	make dev-db
	make django-migrate
	./manage.py createsuperuser
	make django-server

django-test:
	./manage.py test

requirements:

deps-init:
	rm -rf .tox
	$(PIP) install --upgrade pip wheel
	$(PIP) install --upgrade -r requirements/common.txt -r requirements/local.txt -e .
	$(PIP) check

deps-update:
	$(PIP) install --upgrade pip-tools pip wheel
	$(PIP)-tools compile --upgrade --resolver backtracking -o ./requirements/common.txt pyproject.toml
	$(PIP)-tools compile --extra dev --upgrade --resolver backtracking -o ./requirements/local.txt pyproject.toml


build:
	$(PIP) install --upgrade setuptools wheel twine
	$(PIP) install --upgrade build

	if [ -d "./build" ]; then sudo rm -r build; fi
	if [ -d "./dist" ]; then sudo rm -r dist; fi
	if [ -d "./django_memberpress_client.egg-info" ]; then sudo rm -r django_memberpress_client.egg-info; fi

	$(PYTHON) -m build --sdist ./
	$(PYTHON) -m build --wheel ./

	$(PIP) install --upgrade twine
	twine check dist/*


# -------------------------------------------------------------------------
# upload to PyPi Test
# https:// ?????
# -------------------------------------------------------------------------
release-test:
	git rev-parse --abbrev-ref HEAD | grep '^main$' || (echo 'Not on main branch, aborting' && exit 1)
	make build
	twine upload --verbose --skip-existing --repository testpypi dist/*


# -------------------------------------------------------------------------
# upload to PyPi
# https://pypi.org/project/django-memberpress-client/
# -------------------------------------------------------------------------
release-prod:
	git rev-parse --abbrev-ref HEAD | grep '^main$' || (echo 'Not on main branch, aborting' && exit 1)
	make build
	twine upload --verbose --skip-existing dist/*

######################
# HELP
######################

help:
	@echo '===================================================================='
	@echo 'pre-commit		- install and configure pre-commit hooks'
	@echo 'requirements		- install Python, npm and pre-commit requirements'
	@echo 'init			- build virtual environment and install requirements'
	@echo 'clean			- destroy all build artifacts'
	@echo 'repository		- runs cloc report'
	@echo 'build			- build the project'
	@echo 'release-test		- test deployment to PyPi'
	@echo 'release-prod		- production deployment to PyPi'
