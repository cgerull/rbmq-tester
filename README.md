# rbmq-tester

Test producer and consumer of RabbitMQ .

## Configuration

Both components use a common configuration module.

The defaults are basic, but enought to test an arbitrary RabbitMQ vhost. 
Configuration can be done in two flavours: first use the mq_test.yml and set the 
desired configurtion or use envrionment variables.

The precedence is (high to low):
environment -> config file -> build-in defaults

### default values

```python
'host': 'localhost',
'port': 5672,
'user': 'guest',
'pw': 'guest',
'vhost': '/testing',
'exchange': '',
'queue': 'hello-MQ',
'endless': True
```

### mq_test.yml

```yaml
  host: localhost
  user: rbmq_user
  pw: rbmq_pass
  queue: testQ
```

### environment variables

In this version the following environment variables are supported:

```bash
RBMQ_HOST
RBMQ_USER
RBMQ_PASS
RBMQ_QUEUE
RBMQ_EXCHG
```

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
