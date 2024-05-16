#!/usr/bin/env python3
"""Web utilities"""

import redis
import requests

redis_client = redis.Redis()

def get_page(url: str) -> str:
    """
    Retrieve HTML content of the given URL.
    
    Args:
        url (str): The URL to retrieve content from.
    
    Returns:
        str: The HTML content of the URL.
    """
    redis_client.incr(f"count:{url}")
    cached_response = redis_client.get(f"cached:{url}")

    if cached_response:
        return cached_response.decode('utf-8')

    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        redis_client.setex(f"cached:{url}", 10, content.encode('utf-8'))
        return content
    else:
        return f"Error: {response.status_code}"
