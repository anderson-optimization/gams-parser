FROM andersonopt/ao-python

ENV TASKPATH /var/task
WORKDIR $TASKPATH

# Copy dependencies
COPY gams.exe /tmp/gams.exe

# Install GAMS
ENV GAMSFOLDER gams27.1_linux_x64_64_sfx
ENV GAMSPATH ${TASKPATH}/${GAMSFOLDER}

RUN chmod +x /tmp/gams.exe && /tmp/gams.exe && rm /tmp/gams.exe
RUN ln -s $GAMSPATH gams

# Setup python bindings
RUN apt-get update && apt-get install -y python-dev

WORKDIR ${GAMSPATH}/apifiles/Python/api_36

RUN python3 setup.py install
ENV LD_LIBRARY_PATH ${GAMSPATH}

WORKDIR $TASKPATH


#Install gdxpds
# Encoding error on install https://github.com/attilaolah/diffbot.py/issues/13
ENV LC_CTYPE C.UTF-8
RUN \
 pip3 install gdxpds -t .pypath/ 

COPY gdx_to_csv.py /bin/gdx_to_csv.py
COPY format.json $TASKPATH/format.json

RUN chmod +x /bin/gdx_to_csv.py

WORKDIR /root

CMD ['gdx_to_csv.py']

