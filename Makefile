clean: clean-pyc clean-build clean-test ## remove all build, test, coverage and Python artifacts

runprocess: test lint precommit clean

test: # run tests for django api
	uv run pytest

clean-build: # remove build artifacts
	rm -rf -f build/
	rm -rf -f dist/
	rm -rf -f .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: # remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.DS_Store' -exec rm -fr {} +

clean-test: # remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

migrate: # run django migrations & migrate
	uv run python manage.py makemigrations
	uv run python manage.py migrate

coverage: # run the coverage checks
	uv run coverage run -m pytest
	uv run coverage report
	uv run coverage html

install: # install the project dependencies
	uv install

precommit: # run the pre-commit hook
	uv run pre-commit run --all-files

run: # run the django server
	uv run python manage.py runserver 0.0.0.0:${port}

run-celery: # run the celery worker
	uv run celery -A core worker -l info

format:
	uv run ruff format .

lint: # lint the codes
	uv run ruff check --fix .
	uv run ruff format .
	uv run pre-commit run --all-files -c .pre-commit-config.yaml

export: # export the requirements.txt
	uv export --no-hashes --no-annotate -o requirements.txt
