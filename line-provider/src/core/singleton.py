class _SingletonWrapper:
    def __init__(self, cls):
        self._instance = None
        self.__wrapped = cls

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self.__wrapped(*args, **kwargs)
        return self._instance


def singleton(cls):
    return _SingletonWrapper(cls)
