
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



test: test_parse test_inject test_transform	

test_parse:
	python  ${NOSETEST} -v ${FLAGS} test/parse/*.py

test_inject:
	python  ${NOSETEST} -v ${FLAGS} test/inject/*.py

test_transform:
	python  ${NOSETEST} -v ${FLAGS} test/transform/*.py

test_verbose:
	make FLAGS="--nocapture" test


.PHONY: init test