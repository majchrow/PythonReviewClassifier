#!/usr/bin/env python3

from functools import wraps


def singleton(class_):
    """Singleton wrapper to enable having only one instance of chosen class"""
    instances = {}

    @wraps(class_)
    def wrapper():
        if class_ not in instances:
            instances[class_] = class_()
        return instances[class_]

    return wrapper
