from kombu.mixins import ConsumerProducerMixin, ConsumerMixin

from utilitarian_queue_consumer.conf import settings


class UtilitarianConsumer(ConsumerMixin):

    def __init__(self, connection, exchanges, queues):
        self.connection = connection
        self.exchanges = exchanges
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        consume_from = list()
        for queue in settings.CONSUME_FROM:
            consume_from.append(self.queues.get(queue))
        consumer = [Consumer(queues=consume_from, on_message=self.on_message,
                             prefetch_count=settings.PREFETCH_COUNT)]
        return consumer

    def on_message(self, message):
        pass


class UtilitarianProducingConsumer(ConsumerProducerMixin, UtilitarianConsumer):
    """"""
    pass


