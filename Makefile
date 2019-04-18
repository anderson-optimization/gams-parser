
NOSETEST=$(shell which nosetests)
all:
	echo "Test"

init:
	pip install -r requirements.txt

test:
	python  ${NOSETEST} -v test/**/*.py

.PHONY: init test