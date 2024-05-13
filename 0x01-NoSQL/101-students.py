#!/usr/bin/env python3
'''
A function to find and return the top students from a MongoDB collection
based on their average scores in specific topics.
'''


def top_students(mongo_collection):
    '''
    This function takes a MongoDB collection as input and returns
    a cursor to the top students based on their average scores.
    '''
    top_student = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_student
