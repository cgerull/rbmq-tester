# rbmq-tester

Test producer and consumer of RabbitMQ .

## Configuration

Both components use a common configuration module.

The defaults are basic, but enough to test an arbitrary RabbitMQ vhost.
Configuration can be done in two flavours: first use the mq_test.yml and set the
desired configuration or use environment variables.

The precedence of config variables is (high to low):

_environment -> config file -> build-in defaults_

### Default values

```python
'host': 'localhost',
'port': 5672,
'user': 'guest',
'pw': 'guest',
'vhost': '/testing',
'exchange': '',
'queue': 'hello-MQ',
'payload': '',
'interval': None,
'endless': True
```

### rbmq_tester.yml example

```yaml
  host: localhost
  user: rbmq_user
  pw: rbmq_pass
  queue: testQ
```

### Environment variables

In this version the following environment variables are supported:

| Variable      | Description                                          |
|---------------|------------------------------------------------------|
| RBMQ_HOST     | RabbitMQ host, if run from container the Docker host |
| RBMQ_USER     | username                                             |
| RBMQ_PASS     | password                                             |
| RBMQ_QUEUE    | queue name, will be created if not existing          |
| RBMQ_EXCHG    | Exchange name, default to AMQP default               |
| RBMQ_PAYLOAD  | File name for payload file                           |
| RBMQ_INTERVAL | Interval in seconds of message sent                  |

## Producer

The producer connects to the exchange with the configured parameters.
As a test payload the current timestamp is send to the queue. With the
parameter endless = True it will repeat until the producer receives a
CTRL-C keystroke.

In the next a configurable payload is planned.

## Consumer

The consumer connects to the configured exchange and reads the queue.
Again it will read the queue and print the received content until the
process is terminated with CTRL-C.

## Running as Docker containers

Build with

```bash
docker build -t rbmq-tester:<tag> .
```

Run with

```bash
docker run -d --rm \
   --name rbmq-tester \
   -e MODE=<produce | consume> \
   -e RBMQ_HOST=<myhost> \
   rbmq-tester:<tag>
```

Use one of the enclosed docker-composs files as an example.

## Run local

Best to run in a Python virtual environment. Use python 3.7 or higher.

Install python virtual environment

```python -m venv venv```

And run on Linux or MacOs with 
```source venv/bin/activate```

or on Windows with
```venv\script\activate\.bat```

Now edit your rbmq-tester.yml and run rbmq-tester with

```bash
venv $ python rbmq-tester.py produce
```
