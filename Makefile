# -------------------------------------------------------------------------
# build a package for PyPi
# -------------------------------------------------------------------------
SHELL := /bin/bash
export

ifeq ($(OS),Windows_NT)
    PYTHON := python.exe
    ACTIVATE_VENV := venv\Scripts\activate
else
    PYTHON := python3.11
    ACTIVATE_VENV := source venv/bin/activate
endif
PIP := $(PYTHON) -m pip

ifneq ("$(wildcard .env)","")
endif

.PHONY: build requirements deps-update deps-init

dev-db:
	mysql -uroot -p < memberpress_client/scripts/init-db.sql

dev-up:
	brew services start mysql
	brew services start redis

dev-down:
	brew services stop mysql
	brew services stop redis

# ---------------------------------------------------------
# Python
# ---------------------------------------------------------
check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo >&2 "This project requires $(PYTHON) but it's not installed.  Aborting."; exit 1; }

python-init:
	make check-python
	make python-clean && \
	$(PYTHON) -m venv venv && \
	$(ACTIVATE_VENV) && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r requirements/local.txt

python-lint:
	make check-python
	make pre-commit-run

python-clean:
	rm -rf venv
	find ./ -name __pycache__ -type d -exec rm -rf {} +


django-server:
	$(PYTHON) ./manage.py runserver 0.0.0.0:8000

django-migrate:
	$(PYTHON) ./manage.py migrate
	$(PYTHON) ./manage.py makemigrations memberpress_client
	$(PYTHON) ./manage.py migrate memberpress_client

django-shell:
	$(PYTHON) ./manage.py shell_plus


django-quickstart:
	pre-commit install
	make requirements
	make dev-up
	make dev-db
	make django-migrate
	$(PYTHON) ./manage.py createsuperuser
	make django-server

django-test:
	$(PYTHON) ./manage.py test

requirements:
	pre-commit autoupdate
	$(PIP) install --upgrade pip wheel pip-tools
	pip-compile requirements/common.in
	pip-compile requirements/local.in
	$(PIP) install -r requirements/common.txt
	$(PIP) install -r requirements/local.txt

deps-init:
	rm -rf .tox
	$(PIP) install --upgrade pip wheel
	$(PIP) install --upgrade -r requirements/common.txt -r requirements/local.txt -e .
	$(PIP) check

deps-update:
	$(PIP) install --upgrade pip-tools pip wheel
	$(PYTHON) -m piptools compile --upgrade --resolver backtracking -o ./requirements/common.txt pyproject.toml
	$(PYTHON) -m piptools compile --extra dev --upgrade --resolver backtracking -o ./requirements/local.txt pyproject.toml


report:
	cloc $(git ls-files)


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
	make build
	twine upload --verbose --skip-existing --repository testpypi dist/*


# -------------------------------------------------------------------------
# upload to PyPi
# https://pypi.org/project/django-memberpress-client/
# -------------------------------------------------------------------------
release-prod:
	make build
	twine upload --verbose --skip-existing dist/*
