FROM python:3.7-alpine

WORKDIR /usr/src/app

ENV MODE=produce
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python ./rbmq-test.py ${MODE}
