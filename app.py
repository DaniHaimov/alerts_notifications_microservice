import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

_channel = None


def _def_callback(ch, method, properties, body):
    event_data = json.loads(body)
    __alerts_n_notifications.process_event(event_data)


class AlertsAndNotifications:
    def __init__(self,
                 channel,
                 name: str,
                 callback_func=_def_callback):
        self.__rules = {
            'ADD_RULE': self.add_rule
        }
        self.__channel = channel
        self.__channel.basic_consume(queue=name, on_message_callback=callback_func, auto_ack=True)

    def start(self):
        self.__channel.start_consuming()

    def add_rule(self, event_data):
        rule_key = event_data.get('rule_key')
        msg = event_data.get('message')
        self.__rules.update({rule_key: lambda x: print(msg)})

    def default_handler(self, event_data):
        event = event_data.get('event', None)
        if event.startswith('RULE'):
            rule_num = event[4:]
            handler = (lambda: print(f'WARNING{rule_num}'))
        else:
            handler = self.__rules.get(event, lambda: print(f'{event}: Unknown rule'))
        handler()

    def process_event(self, event_data):
        event_key = event_data.get('event', None)
        rule = self.__rules.get(event_key, self.default_handler)
        rule(event_data)


__alerts_n_notifications: AlertsAndNotifications

if __name__ == '__main__':
    print("DockerInit")
    msg_broker_host = os.getenv("MESSAGE_BROKER_CONSUMER_HOST")
    msg_broker_port = int(os.getenv("MESSAGE_BROKER_CONSUMER_PORT"))
    msg_broker_name = os.getenv("MESSAGE_BROKER_CONSUMER_NAME")

    amqp_url = f'amqp://guest:guest@{msg_broker_host}:{msg_broker_port}/%2F'

    params = pika.URLParameters(amqp_url)
    # params = pika.ConnectionParameters(host=msg_broker_host, port=msg_broker_port)

    connection = pika.BlockingConnection(params)
    _channel = connection.channel()
    _channel.queue_declare(queue=msg_broker_name)

    __alerts_n_notifications = AlertsAndNotifications(channel=_channel,
                                                      name=msg_broker_name,
                                                      callback_func=_def_callback)

    print(os.getenv("STARTING_MSG").format(msg_broker_host, msg_broker_port, msg_broker_name))
    __alerts_n_notifications.start()
