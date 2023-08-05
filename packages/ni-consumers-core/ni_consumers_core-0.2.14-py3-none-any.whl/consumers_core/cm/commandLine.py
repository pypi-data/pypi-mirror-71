import json

import click
import coloredlogs
import pika

from ..consumer import ReconnectingExampleConsumer
from .main import load_consumer_file, find_consumer_file


@click.command(name='consumer')
@click.option('--file', '-f', default='consumer.py', required=True, help='Consumer file action')
@click.option('--log-level', '-l', default='INFO', help='Log level')
@click.option('--amqp-username', '-u', default='guest', help='AMQP Username')
@click.option('--amqp-password', '-p', default='guest', help='AMQP Password')
@click.option('--amqp-url', '-r', default='localhost', help='AMQP url')
@click.option('--amqp-port', '-P', default=5672, help='AMQP port')
@click.option('--queue-name', '-q', required=True, help='queue name to observe')
def cm(file, log_level, amqp_username, amqp_password, amqp_url, amqp_port, queue_name):
    coloredlogs.install(level=log_level)

    # Load implementation
    consumer_file = find_consumer_file(file)
    _,action_class = load_consumer_file(consumer_file)

    action = action_class[list(action_class.keys())[1]]()

    # Send registration message
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(amqp_url, amqp_port, '/', credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue='registration',
                          durable=True,
                          arguments={'x-dead-letter-exchange': '',
                                     'x-dead-letter-routing-key': 'registration.dead-letter.queue'},
                          exclusive=False,
                          auto_delete=False)

    channel.confirm_delivery()

    channel.basic_publish(exchange='registration.exchange',
                          routing_key='registration.routing',
                          body=json.dumps({"name": action.name, "category": action.category}),
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                              content_type='text/plain'
                          ))

    amqp_url_joined = f'amqp://{amqp_username}:{amqp_password}@{amqp_url}:{amqp_port}/%2F'
    consumer = ReconnectingExampleConsumer(amqp_url_joined, queue_name, action)
    consumer.run()
