FROM alpine:3.12.1

# Run as a producer by default
ENV MODE=produce

WORKDIR /usr/src/app

# COPY requirements.txt ./
COPY . .

RUN apk add --update --no-cache python3 \
 && pip3 install --update pip \
 && pip3 install --no-cache-dir -r requirements.txt
# WORKDIR /usr/src/app


# COPY requirements.txt ./
# RUN pip3 install --update pip \
#  && pip3 install --no-cache-dir -r requirements.txt

# COPY . .

CMD python3 ./rbmq-tester.py ${MODE}
