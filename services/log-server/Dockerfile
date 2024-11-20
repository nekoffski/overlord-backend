FROM python:3.12
WORKDIR /overlord-log-server/

COPY src /overlord-log-server/src
COPY dist /overlord-log-server/dist
COPY requirements.txt /overlord-log-server/
COPY spawn.sh /overlord-log-server/

RUN mkdir /overlord-log-server/log
RUN touch /overlord-log-server/log/logs.txt

RUN python -m pip install /overlord-log-server/dist/*.gz
RUN python -m pip install -r ./requirements.txt
CMD ["./spawn.sh"]
