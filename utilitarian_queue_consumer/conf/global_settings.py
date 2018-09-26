"""
Global settings
"""

DEBUG = False

AMQP_CONNECTION_STRING = 'amqp://guest:guest@localhost:5672//'

EXCHANGES = {}

QUEUES = {}

CONSUME_FROM = []

PREFETCH_COUNT = 1

WORKER_CLASS = None


# TODO: Handle settings of logging!
