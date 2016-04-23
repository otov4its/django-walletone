from walletone import settings


class override_settings(object):
    """
    Acts as a context manager. It's used with the ``with`` statement.
    """
    def __init__(self, **kwargs):
        self.options = kwargs
        self.original_values = {}
        for key, new_value in kwargs.items():
            self.original_values[key] = getattr(settings, key)

    def __enter__(self):
        for key, new_value in self.options.items():
            setattr(settings, key, new_value)

    def __exit__(self, exc_type, exc_value, traceback):
        for key, original_value in self.original_values.items():
            setattr(settings, key, original_value)