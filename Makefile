
IMAGE="andersonopt/task-gams-parser"
NOSETEST=$(shell which nosetests)
all:
	echo "Test"

init:
	pip install -r requirements.txt

build:
	docker build -t ${IMAGE} .

deploy:
	docker push ${IMAGE}

inspect:
	docker run -it --rm ${IMAGE} /bin/bash



test: test_parse test_inject test_transform	test_gams_parser test_inject

## Test categories

test_parse:
	python  ${NOSETEST} -v ${FLAGS} test/parse/*.py

test_inject:
	python  ${NOSETEST} -v ${FLAGS} test/inject/inject*.py

test_transform:
	python  ${NOSETEST} -v ${FLAGS} test/transform/transform_add.py

test_gams_parser:
	python  ${NOSETEST} -v ${FLAGS} test/gams_parser/*.py

## Individuals

test_real:
	python  ${NOSETEST} -v ${FLAGS} test/parse/real.py

test_equation:
	python  ${NOSETEST} -v ${FLAGS} test/transform/transform_equation.py

test_to_json:
	python  ${NOSETEST} -v ${FLAGS} test/transform/transform_dict.py

test_set:
	python  ${NOSETEST} -v ${FLAGS} test/parse/set.py




test_verbose:
	make FLAGS="--nocapture" test


.PHONY: init test