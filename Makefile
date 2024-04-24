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
	./manage.py runserver 0.0.0.0:8000

django-migrate:
	./manage.py migrate
	./manage.py makemigrations memberpress_client
	./manage.py migrate memberpress_client

django-shell:
	./manage.py shell_plus


django-quickstart:
	pre-commit install
	make requirements
	make dev-up
	make dev-db
	make django-migrate
	./manage.py createsuperuser
	make django-server

django-test:
	./manage.py test

requirements:
	pre-commit autoupdate
	python3 -m pip install --upgrade pip wheel
	pip-compile requirements/common.in
	pip-compile requirements/local.in
	pip install -r requirements/common.txt
	pip install -r requirements/local.txt

deps-init:
	rm -rf .tox
	python3 -m pip install --upgrade pip wheel
	python3 -m pip install --upgrade -r requirements/common.txt -r requirements/local.txt -e .
	python3 -m pip check

deps-update:
	python3 -m pip install --upgrade pip-tools pip wheel
	python3 -m piptools compile --upgrade --resolver backtracking -o ./requirements/common.txt pyproject.toml
	python3 -m piptools compile --extra dev --upgrade --resolver backtracking -o ./requirements/local.txt pyproject.toml


report:
	cloc $(git ls-files)


build:
	python3 -m pip install --upgrade setuptools wheel twine
	python3 -m pip install --upgrade build

	if [ -d "./build" ]; then sudo rm -r build; fi
	if [ -d "./dist" ]; then sudo rm -r dist; fi
	if [ -d "./django_memberpress_client.egg-info" ]; then sudo rm -r django_memberpress_client.egg-info; fi

	python3 -m build --sdist ./
	python3 -m build --wheel ./

	python3 -m pip install --upgrade twine
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
