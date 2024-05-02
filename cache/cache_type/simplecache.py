from cache.cache_type.basecache import BaseCache
import typing as _t


class SimpleCache(BaseCache):

    def __init__(
            self,
            threshold: int = 500,
            default_timeout: int = 300
    ):
        BaseCache.__init__(self, default_timeout)
        self._cache = _t.Dict[str, _t.Any] = {}
        self._threshold = threshold or 500

    def _over_threshold(self) -> bool:
        return len(self._cache) > self._threshold

    def _remove_expired(self, now: float) -> None:
        to_remove = [k for k, (expires, _) in self._cache.items() if expires < now]
        for k in to_remove:
            self._cache.pop(k, None)
