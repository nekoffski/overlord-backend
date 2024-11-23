
FROM python:3.12

WORKDIR /overlord-device-gateway/

COPY src /overlord-device-gateway/src
COPY dist /overlord-device-gateway/dist
COPY requirements.txt /overlord-device-gateway/
COPY spawn.sh /overlord-device-gateway/

RUN python -m pip install /overlord-device-gateway/dist/*.gz
RUN python -m pip install -r ./requirements.txt
CMD ["./spawn.sh"]
