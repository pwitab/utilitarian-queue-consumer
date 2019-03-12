import importlib
import os

from utilitarian_queue_consumer.conf import global_settings

ENVIRONMENT_VARIABLE = "SETTINGS_MODULE"


class ImproperlyConfigured(Exception):
    """Application is improperly configured"""
    pass


class Settings:
    """
    Class for storing all application settings. Inspired by Django settings
    """

    def __init__(self):
        pass

    def configure(self):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)

        if not settings_module:
            raise ImproperlyConfigured(
                'Environment variable,{0} , for settings module '
                'is not set'.format(ENVIRONMENT_VARIABLE))

        self._setup(settings_module)

    def _setup(self, settings_module):

        # Load the global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        # TODO: How do we add global (default) settings for 3d party stuff?

        self.SETTINGS_MODULE = settings_module

        module = importlib.import_module(self.SETTINGS_MODULE)

        for setting in dir(module):

            if setting.isupper():  # only care about ALL_CAPS settings
                setattr(self, setting, getattr(module, setting))

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE, }


settings = Settings()
