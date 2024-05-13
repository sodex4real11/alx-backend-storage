#!/usr/bin/env python3
'''A script for retrieving schools by topic from a MongoDB collection.'''


def schools_by_topic(mongo_collection, topic):
    '''
    Retrieve schools from the given Mongo collection based on a specific topic

    Parameters:
    - mongo_collection: The MongoDB collection to search for schools.
    - topic: The topic to filter schools by.

    Returns:
    A list of school documents that match the specified topic.
    '''
    return list(mongo_collection.find({"topics": topic}))
