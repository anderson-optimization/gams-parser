FROM andersonopt/task-ao

WORKDIR /var/task

COPY requirements.txt /var/task/requirements.txt

RUN \
  pip install -r requirements.txt -t .pypath/ 

ADD gams_parser /var/task/.pypath/gams_parser
