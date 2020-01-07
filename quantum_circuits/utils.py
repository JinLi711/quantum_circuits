import functools

from sympy.physics.quantum import TensorProduct

int_to_binary = lambda x, n: format(x, 'b').zfill(n)
tensorproducts = lambda l: functools.reduce(lambda x,y: TensorProduct(x,y), l)