from azure.servicebus import ServiceBusMessage, ServiceBusClient


class AzureMessageBus(object):

    def __init__(self, connection_str: str, queue_name: str):
        self.connection_str = connection_str
        self.queue_name = queue_name
        self.client = ServiceBusClient.from_connection_string(
            conn_str=self.connection_str, logging_enable=True
        )

    def send_single_message(self, event_data):
        sender = self.client.get_queue_sender(queue_name=self.queue_name)
        message = ServiceBusMessage(event_data)
        sender.send_messages(message)

    def send_a_list_of_messages(self, event_data: list):
        sender = self.client.get_queue_sender(queue_name=self.queue_name)
        messages = [ServiceBusMessage(item) for item in event_data]
        sender.send_messages(messages)
