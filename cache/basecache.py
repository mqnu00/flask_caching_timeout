from typing import Any, Optional


class BaseCache:

    def __init__(
            self,
            data: Any,
            threshold: int = 500,
            timeout: int = 600
    ) -> None:
        """

        :param data 数据的逻辑结构:
        :param threshold 数据个数:
        :param timeout 数据有效时间:
        """
        self.data = data
        self.threshold = threshold
        self.timeout = timeout

    def get(self, key: str) -> Any:
        """查找 key 对应的 value。

        :param key:
        :return: 如果不存在，返回None
        """
        return None

    def delete(self, key: str) -> bool:
        """删除数据。

        :param key:
        :return: True 删除成功
        """
        return True

    def set(self, key: str, value: Any) -> Optional[bool]:
        """设置新的数据，会覆盖重复的 key。

        :param key :
        :param value:
        :return: True 表示数据更新成功
        """
        return True

    def add(self, key: str, value: Any) -> bool:
        """和 set 类似，但是不会覆盖重复的 key

        :param key:
        :param value:
        :return:
        """
        return True

    def has(self, key: str) -> bool:
        """判断 key 是否存在，这不需要加载实际数据，能够提升性能

        :param key:
        :return:
        """
        raise NotImplementedError(
            "%s 没有 has 的实现方法，这意味着无法判断 key 是否存在，"
            "你可以尝试 get 方法"
        )

    def clear(self) -> bool:
        """清除所有缓存数据，但并不是所有缓存类型都支持

        :return:
        """
        return True


