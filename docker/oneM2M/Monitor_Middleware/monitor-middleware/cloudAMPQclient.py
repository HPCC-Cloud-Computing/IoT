__author__ = 'huanpc'

import rabbitpy
import os


API_KEY = ''
if os.environ.get('AMPQ_API_KEY'):
    API_KEY = os.environ['AMPQ_API_KEY']


def publish_message(message, queue_name='hello'):
    if API_KEY:
        rabbitpy.publish(API_KEY, exchange_name='', routing_key=queue_name, body=message)
        return True
    else:
        return False


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

