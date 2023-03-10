from azure.servicebus import ServiceBusClient

from optym_poc.core.config import settings


def read_message():
    print(settings.MESSAGEBUS_CONNECTION_STRING)
    client = ServiceBusClient.from_connection_string(
        conn_str=settings.MESSAGEBUS_CONNECTION_STRING, logging_enable=True
    )
    receiver = client.get_queue_receiver(
        queue_name=settings.MESSAGEBUS_QUEUE_NAME, max_wait_time=30
    )
    with receiver:
        for msg in receiver:
            print("Received: " + str(msg))


if __name__ == "__main__":
    read_message()
