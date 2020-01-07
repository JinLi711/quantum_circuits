from warnings import warn

from sympy import *

warn_untested = lambda x: warn('({}) is not yet tested yet.'.format(x))

def U3_gate(phi, theta, lambda_):
    gate = Matrix([
        [E ** (-I * (phi + lambda_) / 2.0) * cos(theta / 2.0), 
         -E ** (-I * (phi - lambda_) / 2.0) * sin(theta / 2.0)],
        [E ** (I * (phi - lambda_) / 2.0) * sin(theta / 2.0), 
         E** (I * (phi + lambda_) / 2.0) * cos(theta / 2.0)]
        ])
    return gate


def CX_gate():
    gate = Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    return gate


def U2_gate(phi, lambda_):
    return U3_gate(phi, pi / 2.0, lambda_)


def U1_gate(lambda_):
    # includes phase shift
    return exp(0.5*I*lambda_) * U3_gate(0.0, 0.0, lambda_)


def RX_gate(theta):
    return Matrix(simplify(U3_gate(-pi / 2.0, theta, pi / 2.0)))


def RY_gate(theta):
    return Matrix(simplify(U3_gate(0.0, theta, 0.0)))


def RZ_gate(theta):
    return U1_gate(theta)


def X_gate():
    # includes phase shift
    return Matrix(simplify(I * U3_gate(0, pi, pi)))


def ID_gate():
    return Matrix(simplify(U3_gate(0, 0, 0)))


def Y_gate():
    warn_untested('Y_gate')
    gate = Matrix([
        [0, I],
        [-I, 0]
        ])
    return gate


def Z_gate():
    warn_untested('Z_gate')
    gate = Matrix([
        [1, 0],
        [0, -1]
        ])
    return gate


def H_gate():
    # includes phase shift
    return Matrix(simplify(I * U2_gate(0, pi)))
