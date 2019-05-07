
IMAGE="andersonopt/gdxpandas"

all:
	echo "Test"

build: gams.exe
	docker build -t ${IMAGE} .

gams.exe: 
	curl -o gams.exe https://d37drm4t2jghv5.cloudfront.net/distributions/27.1.0/linux/linux_x64_64_sfx.exe

deploy:
	docker push ${IMAGE}

inspect:
	docker run -it --rm ${IMAGE} /bin/bash

clean:
	rm gams.exe