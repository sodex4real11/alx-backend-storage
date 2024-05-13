#!/usr/bin/env python3
'''A script for listing all documents in a MongoDB collection.'''


def list_all(mongo_collection):
    '''
    Lists all documents in the given MongoDB collection.

    Parameters:
    - mongo_collection: The MongoDB collection to retrieve documents from.

    Returns:
    A list of documents from the collection or empty list if no documents
    '''
    documents = mongo_collection.find()

    if documents.count() == 0:
        return []
    return documents
