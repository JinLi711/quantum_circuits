import functools

from sympy.physics.quantum import TensorProduct
from sympy import *
import numpy as np

# compute the tensor product of a list of matrixes / vectors
tensorproducts = lambda l: functools.reduce(lambda x,y: TensorProduct(x,y), l)


def sp_to_np(x):
    """convert Sympy to numpy array"""

    return np.array(x).astype(np.float64)

def int_to_binary(x, n):
    """Convert an integer into its binary representation

    Args:
        x (int): input integer
        n (int): number of leading zeros to display

    Returns:
        (str) binary representation
    """

    if type(x) != int:
        raise ValueError('x must be an integer.')
    return format(x, 'b').zfill(n)


def bit_to_matrix(x):
    if x == '0':
        return Matrix([1, 0])
    elif x == '1':
        return Matrix([0, 1])
    else:
        raise ValueError('Bit must be either 0 or 1.')