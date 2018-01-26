.PHONY: build test start

build:
	pipenv install --dev

test:
	pipenv check --style ./ras_backstage ./test
	pipenv run python run_tests.py

start:
	pipenv run python run.py
