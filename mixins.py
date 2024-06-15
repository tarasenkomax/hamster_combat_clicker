from time import time


class TimestampMixin:
    @staticmethod
    def timestamp() -> int:
        return int(time())
