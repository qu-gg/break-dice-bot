"""
@file utils.py
@author

Utility functions for parsing JSON tables
"""


def get_tier(roll, table):
    tier = None
    for key in table.keys():
        lower, upper = [int(i) for i in key.split('-')]
        if lower <= roll <= upper:
            tier = key

    return table[tier]
