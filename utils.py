'''
Utility functions.
'''
import argparse

import numpy as np

# import configs


def read_tsv(filedir: str) -> np.ndarray:
    '''Read the Tab Seperated File and return a np.ndarray'''
    res = []
    with open(filedir, 'r') as f:
        for line in f:
            res.append(line.split())
    return np.array(res)





if __name__ == '__main__':
    pass
