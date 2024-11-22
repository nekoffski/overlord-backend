
FROM python:3.12

WORKDIR /overlord-mi-proxy/

COPY src /overlord-mi-proxy/src
COPY dist /overlord-mi-proxy/dist
COPY requirements.txt /overlord-mi-proxy/
COPY spawn.sh /overlord-mi-proxy/

RUN python -m pip install /overlord-mi-proxy/dist/*.gz
RUN python -m pip install -r ./requirements.txt
CMD ["./spawn.sh"]
