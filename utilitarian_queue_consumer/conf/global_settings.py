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


###########
# LOGGING #
###########

# The callable to use to configure logging
LOGGING_CONFIG = 'logging.config.dictConfig'

# Custom logging configuration.
LOGGING = {}

if DEBUG:
    LOG_LEVEL = 'DEBUG'
else:
    LOG_LEVEL = 'INFO'


# Retry handling on publish
PUBLISH_RETRY = True
PUBLISH_RETRY_INTERVAL_START = 0
PUBLISH_RETRY_INTERVAL_STEP = 2
PUBLISH_RETRY_INTERVAL_MAX = 30
PUBLISH_RETRY_MAX_RETRIES = 30


