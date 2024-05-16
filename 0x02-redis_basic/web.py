
#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def count_requests(method: Callable) -> Callable:
    """A decorator function to count the number of requests made to a given URL
    and cache the response using Redis.
    """
    @wraps(method)
    def invoker(url) -> str:
        """ Wrapper for decorator """
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@count_requests
def get_page(url: str) -> str:
    """Retrieve the content of a given URL using the requests library.
    """
    return requests.get(url).text
