import functools

from sympy.physics.quantum import TensorProduct
from sympy import *

int_to_binary = lambda x, n: format(x, 'b').zfill(n)
tensorproducts = lambda l: functools.reduce(lambda x,y: TensorProduct(x,y), l)

def bit_to_matrix(x):
    if x == '0':
        return Matrix([1, 0])
    elif x == '1':
        return Matrix([0, 1])
    else:
        raise ValueError('Bit must be either 0 or 1.')