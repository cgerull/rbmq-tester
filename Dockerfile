FROM alpine:3.10.2

RUN apk add --no-cache python3 

WORKDIR /usr/src/app

# Run as a producer by default
ENV MODE=produce
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD python3 ./rbmq-tester.py ${MODE}
