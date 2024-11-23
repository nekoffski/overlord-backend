
FROM python:3.12

WORKDIR /overlord-yeelight-connector/

COPY src /overlord-yeelight-connector/src
COPY dist /overlord-yeelight-connector/dist
COPY requirements.txt /overlord-yeelight-connector/
COPY spawn.sh /overlord-yeelight-connector/

RUN python -m pip install /overlord-yeelight-connector/dist/*.gz
RUN python -m pip install -r ./requirements.txt
CMD ["./spawn.sh"]
