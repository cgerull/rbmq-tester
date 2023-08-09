FROM alpine:3.18

# Run as a producer by default
ENV MODE=produce

WORKDIR /usr/src/app

# COPY requirements.txt ./
COPY . .

RUN apk add --update --no-cache \
    python3 \
    py3-pip \
 && pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && adduser --disabled-password tester && chown -R tester.tester /usr/src/app

USER tester

CMD python3 ./rbmq-tester.py ${MODE}
