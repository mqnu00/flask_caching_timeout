import time

from cache.cache_type.basecache import BaseCache
from cachelib.serializers import SimpleSerializer
import typing as _t


class SimpleCache(BaseCache):
    serializer = SimpleSerializer()

    def __init__(
            self,
            threshold: int = 500,
            frequency: int = 30,
            default_timeout: int = 300,
            enable_ttl: bool = True,
            refresh_type: str = 'FIFO'
    ):
        """

        :param threshold:
        :param default_timeout:
        :param enable_ttl: 是否使用缓存过期策略
        :param refresh_type: 使用什么缓存算法 FIFO LRU LFU
        """
        BaseCache.__init__(self, default_timeout)
        self._cache: _t.Dict[str, _t.Any] = {}
        self._threshold = threshold or 500
        self._frequency = frequency or 30
        self._refresh_type = refresh_type

    def _over_threshold(self) -> bool:
        return len(self._cache) > self._threshold

    def _remove_expired(self, now: float) -> None:
        """TTL

        :param now:
        :return:
        """
        to_remove = [k for k, (expires, _) in self._cache.items() if expires < now]
        for k in to_remove:
            self._cache.pop(k, None)

    def _remove_older(self) -> None:

        """FIFO

        :return:
        """
        k_ordered = (
            k for k, v in sorted(
            self._cache.items(), key=lambda item: item[1][0]
        )
        )

        for k in k_ordered:
            self._cache.pop(k, None)
            if not self._over_threshold():
                break

    def _remove_low_frequency(self) -> None:
        pass

    def _normalize_timeout(self, timeout: _t.Optional[int]) -> int:
        timeout = BaseCache._normalize_timeout(self, timeout)
        if timeout > 0:
            timeout = int(time.time()) + timeout
        return timeout

    def set(self, key: str, value: _t.Any, timeout: _t.Optional[int] = None) -> _t.Optional[bool]:
        if self._refresh_type == 'FIFO':
            expires = self._normalize_timeout(timeout)
            self._cache[key] = (expires, self.serializer.dumps(value))
        elif self._refresh_type == 'LFU':
            frequency = 0
            self._cache[key] = [frequency, self.serializer.dumps(value)]
        return True

    def get(self, key: str) -> _t.Any:
        try:
            if self._refresh_type == 'FIFO':
                expires, value = self._cache[key]
                return self.serializer.loads(value)
            elif self._refresh_type == 'LFU':
                frequency, value = self._cache[key]
                frequency = frequency + 1
                self._cache[key] = [frequency, value]
                return self.serializer.loads(value)
        except KeyError:
            return None


if __name__ == '__main__':
    a, b, = [1, 2]
    print(a, b)
