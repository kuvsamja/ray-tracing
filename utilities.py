import random

def random_double(min_val = 0,  max_val = 1):
    return min_val + (max_val-min_val) * random.random()
