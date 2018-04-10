.PHONY: build test start

build:
	pipenv install --dev

lint:
	pipenv run flake8 ./ras_backstage ./test
	pipenv check ./ras_backstage ./test

test: lint
	pipenv run python run_tests.py

start:
	pipenv run python run.py
