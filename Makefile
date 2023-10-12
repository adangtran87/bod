.DEFAULT_GOAL := all

all: lint freeze

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

wsl:
	sudo chown root:dialout /dev/ttyUSB0
	sudo chmod 660 /dev/ttyUSB0
