#!/usr/bin/env python
"""
Collection of utility functions
"""
import numpy as np
import time


def n_fibonacci(n=10):
    """Calculate the Nth Fibonacci number"""
    i = 0
    x = 1
#     print(x)
    for __ in range(n):
        x, i = x + i, x
#         print(x)
    return x

def fake_write(whatevs=None):
    """Take some time as if it were writing to disk/calling a rest API"""
#     long_time = np.random.randint(1,5)
    long_time = 1. + np.random.random()
    time.sleep(long_time)
    return "Done with {} after {} secs".format(whatevs, long_time)

def calc_length(x):
    """Typically x is an int"""
    return len(str(x))

def calc_lengths(iterable_object):
    """Generate lenghts of values from generator.
    
    Works for any iterable.
    """
    for x in iterable_object:
        yield calc_length(x)

def print_stuff(generator_object):
    """Print values as they are generated"""
    for x in generator_object:
        print(x)
