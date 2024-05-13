#!/usr/bin/env python3
'''
This script connects to a MongoDB database, queries an nginx logs collection,
and prints various statistics.
'''
from pymongo import MongoClient

if __name__ == "__main__":
    '''prints statistics related to nginx logs'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs_coll = client.logs.nginx

    total_logs_count = nginx_logs_coll.count_documents({})
    print(f'{total_logs_count} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_logs_coll.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_check = nginx_logs_coll.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{status_check} status check')
