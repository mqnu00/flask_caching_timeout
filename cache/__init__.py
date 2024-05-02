import functools
import pprint

from flask import request, Flask
from typing import Callable, Union, Any


class Cache:

    def __init__(self, app: Flask):
        self.data = dict()
        self.app = app

    def cached(
            self,
            f: Callable,
            threshold: int = 5,
            timeout: int = 600,
            key_redo: Union[str, int] = None,
    ) -> Callable:
        @functools.wraps(f)
        def decorator(*argc, **kwargs):
            if key_redo is None:
                key = 'flask_cache_' + request.path
            else:
                key = 'flask_cache_' + key_redo
            value = self.get(key)
            if value is None:
                value = f(*argc, **kwargs)
                self.set(key, value)
            self.show()
            return value
        return decorator

    def get(self, key: str) -> str | None:
        if key in self.data.keys():
            return self.data[key]
        return None

    def set(self, key: str, value: str) -> None:
        self.data[key] = value

    def show(self):
        pprint.pprint(self.data)