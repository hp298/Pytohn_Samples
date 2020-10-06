"""
Helper functions for k-Means clustering

This file contains the functions for enforcing preconditions for k-means clustering.
We have written the first for you.  You will probably want to write others.

YOUR NAME(S) AND NETID(S) HERE
DATE COMPLETED HERE
"""
import math
import random
import numpy


def is_point(value):
    """
    Returns True if value is a list of int or float
    
    Parameter value: a value to check
    Precondition: value can be anything
    """
    if (type(value) != list):
        return False
    
    # All float
    okay = True
    for x in value:
        if (not type(x) in [int,float]):
            okay = False
    
    return okay


# ADD MORE HELPER FUNCTIONS FOR ASSERTS HERE
def is_point_list(value):
    """
    Returns True if value is a 2d list of int or float
    
    This function also checks that all points in value have same dimension.
    
    Parameter value: a value to check
    Precondition: value can be anything
    """
    if (type(value) != list):
        return False
    elif (len(value) == 0):
        return True
    
    okay = True
    dim = len(value[0])
    for x in value:
        if (len(x) != dim or not is_point(x)):
            okay = False
    
    return okay


def is_seed_list(value, k, size):
    """
    Returns True if value is k-element list of indices between 0 and 1.
    
    Parameter value: a value to check
    Precondition: value can be anything
    
    Parameter k: The required list size
    Precondition: k is an int > 0
    
    Paramater size: The database size
    Precondition: size is an int > 0
    """
    if (type(value) != list):
        return False
    elif (len(value) != k):
        return False
    
    okay = True
    for x in value:
        if type(x) != int or x < 0 or x >= size:
            okay = False
    
    return okay
