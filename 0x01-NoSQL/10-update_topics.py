#!/usr/bin/env python3
'''A script for updating topics in a MongoDB collection.'''


def update_topics(mongo_collection, name, topics):
    '''
    Update topics in the given MongoDB collection for a specific document.

    Parameters:
    - mongo_collection: The MongoDB collection where the update performed
    - name: The name of the document to be updated.
    - topics: The new topics to be set in the document.

    Returns:
    None
    '''
    query = {"name": name}
    update_query = {"$set": {"topics": topics}}
    mongo_collection.update_many(query, update_query)
