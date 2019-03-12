import sys
import logging

import kombu

from utilitarian_queue_consumer.conf import settings
from utilitarian_queue_consumer.utils.module_loading import import_string
from utilitarian_queue_consumer.utils.log import configure_logging

log = logging.getLogger(__name__)


def execute_from_cli(argv=None):
    """
    Configure settings and logging.
    Set up queue connection and set up and declare all echanges and queues.
    """

    settings.configure()

    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)

    # Set up Connection
    connection = kombu.Connection(settings.AMQP_CONNECTION_STRING)

    # Create Exchanges
    exchanges = dict()
    for exchange_name, exchange_settings in settings.EXCHANGES.items():
        exchange = kombu.Exchange(
            name=exchange_name,
            type=exchange_settings.get('type', 'topic'),
            durable=exchange_settings.get('durable', False),
            channel=connection

        )
        exchanges[exchange_name] = exchange
        exchange.declare()

    # Create Queues
    queues = dict()
    for queue_name, queue_settings in settings.QUEUES.items():
        queue = kombu.Queue(name=queue_name,
                            exchange=exchanges.get(
                                queue_settings.get('exchange')
                            ),
                            routing_key=queue_settings.get('routing_key'),
                            channel=connection)

        queues[queue_name] = queue
        queue.declare()

    worker_class = import_string(settings.WORKER_CLASS)
    worker = worker_class(connection, exchanges, queues)

    try:
        worker.run()
    except KeyboardInterrupt:
        sys.exit()
