#!/usr/bin/env python3
'''A script for inserting a school document into a MongoDB collection.'''


def insert_school(mongo_collection, **kwargs):
    '''
    Insert a school document into the given MongoDB collection.

    Parameters:
    - mongo_collection: The MongoDB collection where the document will be inserted.
    - **kwargs: Key-value pairs representing the fields and values of the document to be inserted.

    Returns:
    The object ID of the inserted document.
    '''
    return mongo_collection.insert(kwargs)
