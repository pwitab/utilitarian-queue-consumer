import logging

from kombu.mixins import ConsumerProducerMixin, ConsumerMixin
from kombu.messaging import Consumer, Producer

from utilitarian_queue_consumer.conf import settings

log = logging.getLogger(__name__)


class UtilitarianMessageHandlerError(Exception):
    """An exception occured in """


class UtilitarianConsumer(ConsumerMixin):
    """
    Base class for consumers that are running in Utilitarian
    Define the handle_message method to process a message in a
    subclass of this class.

    If a message makes causes an exception that is not caught in the subclass
    consumer the message will be rejected.
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
            log.exception(e)
            message.reject()
            raise UtilitarianMessageHandlerError() from e

    def handle_message(self, message):
        raise NotImplementedError(
            'handle_message() needs to be implemented in subclass')


class UtilitarianProducingConsumer(ConsumerProducerMixin, UtilitarianConsumer):
    """
    With the producer mixinclass the consumer gets a producer that can publish
    messages available under self.producer
    """

    def handle_message(self, message):
        raise NotImplementedError(
            'handle_message() needs to be implemented in subclass')

    def publish(self, message_body, routing_key, exchange=None):
        """
        Default publish method. Gives good defaults. If you need more control
        override in subclass.
        """

        publish_exchange = exchange or self.producer.exchange

        self.producer.publish(
            body=message_body,
            exchange=publish_exchange,
            routing_key=routing_key,
            retry=settings.PUBLISH_RETRY,
            retry_policy={
                # First retry immediately,
                'interval_start': settings.PUBLISH_RETRY_INTERVAL_START,
                # then increase by 2s for every retry.
                'interval_step': settings.PUBLISH_RETRY_INTERVAL_STEP,
                # but don't exceed 30s between retries.
                'interval_max': settings.PUBLISH_RETRY_INTERVAL_MAX,
                # give up after 30 tries.
                'max_retries': settings.PUBLISH_RETRY_MAX_RETRIES,
                # callback for logging
                'errback': self.on_publish_error,
                'on_revive': self.on_connection_revival
            },
            # declare exchange and queue and bind them
            declare=list(self.queues.values()))  # queues is a dict.
        log.info(f'Published '
                 f'message: {self.producer.exchange.name}::{routing_key}')
        log.debug(f'Published '
                  f'message_body: {message_body}')

    @staticmethod
    def on_publish_error(exc, interval):
        log.exception(f'Connection error during publish, will retry '
                      f'in {interval} seconds', exc_info=exc)

    @staticmethod
    def on_connection_revival(channel):
        log.info(f'Connection to AMQP broker was revived')

    @property
    def producer(self):
        # Giving the producer a default exchange
        return Producer(self.producer_connection,
                        exchange=self.exchanges.get(settings.PUBLISH_TO))
