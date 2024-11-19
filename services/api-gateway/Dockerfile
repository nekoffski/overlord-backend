
FROM python:3.12

WORKDIR /overlord-api-gateway/

COPY src /overlord-api-gateway/src
COPY dist /overlord-api-gateway/dist
COPY requirements.txt /overlord-api-gateway/

RUN python -m pip install /overlord-api-gateway/dist/*.gz
RUN python -m pip install -r ./requirements.txt
CMD ["python", "./src/main.py"]
