.DEFAULT_GOAL := all

all: lint freeze

app:
	python bodpy/bodpy.py

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.spec

env:
	export PYTHONPATH=${PYTHONPATH}:${PWD}

freeze:
	pip freeze > requirements.txt

lint:
	black .
	flake8 .
	mypy .

release:
	flet pack bodpy/bodpy.py

server:
	uvicorn bodpy-server.server:app

wsl:
	sudo chown root:dialout /dev/ttyUSB0
	sudo chmod 660 /dev/ttyUSB0
