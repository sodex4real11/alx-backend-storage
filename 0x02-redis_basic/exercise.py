#!/usr/bin/env python3
"""This module provides a Cache class for caching data in a Redis database.
"""
import redis
from typing import Union, Optional, Callable
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a method is
    called and stores it in Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):

        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that records the inputs and outputs of a method in Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):

        self._redis.rpush(inputs, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(output))
        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Print the call history of a method stored in Redis.

    Args:
        method (Callable): The method to replay and display the call history.
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode('utf-8')
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    """A class for caching data in a Redis database."""
    def __init__(self):
        """
        Initialize a new Cache instance and connect to Redis.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the cache and return a unique key for retrieval.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored

        Returns:
            str: A unique key associated with the stored data.
        """
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from the cache using the provided key.

        Args:
            key (str): The key associated with the data in the cache.
            fn (Optional[Callable]): An optional function to transform
            the retrieved data.

        Returns:
            Union[str, bytes, int, float]: The data retrieved from the cache.
        """
        val = self._redis.get(key)
        if fn:
            val = fn(val)
        return val

    def get_str(self, key: str) -> str:
        """
        Retrieve a string from the cache using the provided key.

        Args:
            key (str): The key associated with the string in the cache.

        Returns:
            str: The string retrieved from the cache.
        """
        val = self._redis.get(key)
        return val.decode('utf-8')

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from the cache using the provided key.

        Args:
            key (str): The key associated with the integer in the cache.

        Returns:
            int: The integer retrieved from the cache. If the data cannot be
            converted to an integer, 0 is returned.
        """
        val = self._redis.get(key)
        try:
            val = int(val.decode('utf-8'))
        except Exception:
            val = 0
        return val
