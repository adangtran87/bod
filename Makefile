.DEFAULT_GOAL := all

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.spec

freeze:
	pip freeze > requirements.txt

lint:
	black .
	flake8 .
	mypy .

release:
	flet pack bodpy/bodpy.py

run:
	python bodpy/bodpy.py

all: lint freeze
