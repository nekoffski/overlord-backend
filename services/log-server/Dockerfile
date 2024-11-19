FROM python:3.12
WORKDIR /overlord-log-server/

COPY *.py /overlord-log-server/
COPY requirements.txt /overlord-log-server/

RUN mkdir /overlord-log-server/log
RUN touch /overlord-log-server/logs.txt

RUN python -m pip install -r ./requirements.txt
CMD ["python", "main.py"]
