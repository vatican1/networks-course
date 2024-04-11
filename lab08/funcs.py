import random

def package_lost(lost_chanse = 0.3):
    return random.uniform(0, 1) <= lost_chanse