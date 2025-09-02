import random

def random_double():
    return random.random()

def random_double_range(min_val,  max_val):
    return min_val + (max_val-min_val) * random_double()
