import logging
import logging.config  # needed when logging_config doesn't start with logging.config

from utilitarian_queue_consumer.utils.module_loading import import_string
from utilitarian_queue_consumer.conf import settings


def get_log_level():
    if settings.DEBUG:
        return 'DEBUG'
    else:
        return 'INFO'

def get_default_logging():
    DEFAULT_LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {

        },
        'formatters': {

            'main_formatter': {
                    'format': '[{asctime}] :: [{levelname}] :: {name} :: {message}',
                    'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': [],
                'class': 'logging.StreamHandler',
                'formatter': 'main_formatter'
            },

        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': get_log_level(),
            },
        }
    }
    return DEFAULT_LOGGING


def configure_logging(logging_config, logging_settings):
    if logging_config:
        # First find the logging configuration function ...
        logging_config_func = import_string(logging_config)

        logging.config.dictConfig(get_default_logging())

        # ... then invoke it with the logging settings
        if logging_settings:
            logging_config_func(logging_settings)
