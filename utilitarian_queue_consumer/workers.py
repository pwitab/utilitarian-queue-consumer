from kombu.mixins import ConsumerProducerMixin, ConsumerMixin

from utilitarian_queue_consumer.conf import settings


class UtilitarianMessageHandlerError(Exception):
    """An exception occured in """


class UtilitarianConsumer(ConsumerMixin):
    """
    Base class for consumers that are running in Utilitarian
    Define the handle_message method to process a message in a
    subclass of this class.
    """

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
        # Kombu has an issue that if an error is an OSError comes in consumers
        # code it will silently eat the error and never raise an exception:
        # https://github.com/celery/kombu/issues/802
        # Workaround for now is to wrap all consumer code in a general
        # try/except and raise an exception if something happens inside the
        # consumer code.

        try:
            self.handle_message(message)
        except Exception as e:
            raise UtilitarianMessageHandlerError() from e

    def handle_message(self, message):
        raise NotImplementedError('This needs to be implemented in subclass')


class UtilitarianProducingConsumer(ConsumerProducerMixin, UtilitarianConsumer):
    """
    With the producer mixinclass the consumer gets a producer that can publish
    messages available under self.producer
    """

    def handle_message(self, message):
        raise NotImplementedError('This needs to be implemented in subclass')
