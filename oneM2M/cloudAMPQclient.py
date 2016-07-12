__author__ = 'huanpc'

import rabbitpy

API_KEY = 'amqp://yhjylhjo:rOYVRlLp47lteZKBJm_2XN02uoy3onKK@white-mynah-bird.rmq.cloudamqp.com/yhjylhjo'


def publish_message(message, queue_name='hello'):
    rabbitpy.publish(API_KEY, exchange_name='', routing_key=queue_name, body=message)


def consume_message(queue_name='hello', all=False):
    with rabbitpy.Connection(API_KEY) as conn:
        with conn.channel() as channel:
            queue = rabbitpy.Queue(channel, queue_name)
            if all:
                # Consume all the message
                for message in queue:
                    message.pprint(True)
                    message.ack()
            else:
                queue[0].pprint(True)
            return queue[0]