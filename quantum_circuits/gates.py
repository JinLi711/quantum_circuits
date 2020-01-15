from sympy import *

import utils

class Gate(object):
    """Gate class for quantum operations.

    Attributes:
        name (str): name of the gate
        indexes (int or list of ints): indexes to perform the quantum gate on
        gate (sympy Matrix): gate operation
        template (str): template for OpenQASM conversion code
    """

    def __init__(self, name, indexes, gate, template):
        self.name = name
        self.indexes = indexes
        self.gate = gate
        self.template = template

    def __call__(self):
        return self.gate

    def __repr__(self):
        return 'Gate.' + self.name + '_gate'


class U3_gate(Gate):
    def __init__(self, phi, theta, lambda_, indexes=None):
        self.phi = phi
        self.theta = theta
        self.lambda_ = lambda_

        gate = Matrix([
            [E ** (-I * (phi + lambda_) / 2.0) * cos(theta / 2.0), 
            -E ** (-I * (phi - lambda_) / 2.0) * sin(theta / 2.0)],
            [E ** (I * (phi - lambda_) / 2.0) * sin(theta / 2.0), 
            E** (I * (phi + lambda_) / 2.0) * cos(theta / 2.0)]
            ])

        template = 'u3({},{},{}) q[{}]'.format(theta, phi, lambda_, indexes)

        Gate.__init__(self, 'U3', indexes, gate, template)


class U2_gate(Gate):
    def __init__(self, phi, lambda_, indexes=None):
        self.phi = phi
        self.lambda_ = lambda_

        gate = U3_gate(phi, pi / 2.0, lambda_)()
        template = 'u2({},{}) q[{}]'.format(phi, lambda_, indexes)

        Gate.__init__(self, 'U2', indexes, gate, template)


class U1_gate(Gate):
    def __init__(self, lambda_, indexes=None):
        self.lambda_ = lambda_

        gate = exp(0.5*I*lambda_) * U3_gate(0.0, 0.0, lambda_)()
        template = 'u1({}) q[{}]'.format(lambda_, indexes)

        Gate.__init__(self, 'U1', indexes, gate, template)


class RX_gate(Gate):
    def __init__(self, theta, indexes=None):
        self.theta = theta

        gate = Matrix(simplify(U3_gate(-pi / 2.0, theta, pi / 2.0)()))
        template = 'rx({}) q[{}]'.format(theta, indexes)

        Gate.__init__(self, 'RX', indexes, gate, template)


class RY_gate(Gate):
    def __init__(self, theta, indexes=None):
        self.theta = theta

        gate = Matrix(simplify(U3_gate(0.0, theta, 0.0)()))
        template = 'ry({}) q[{}]'.format(theta, indexes)

        Gate.__init__(self, 'RY', indexes, gate, template)


class RZ_gate(Gate):
    def __init__(self, theta, indexes=None):
        self.theta = theta

        gate = Matrix(simplify(U1_gate(theta)()))
        template = 'rz({}) q[{}]'.format(theta, indexes)

        Gate.__init__(self, 'RZ', indexes, gate, template)


class ID_gate(Gate):
    def __init__(self, indexes=None):
        gate = Matrix(simplify(U3_gate(0, 0, 0)() ))
        template = 'id q[{}]'.format(indexes)

        Gate.__init__(self, 'ID', indexes, gate, template)

        
class X_gate(Gate):
    def __init__(self, indexes=None):
        gate = Matrix(simplify(I * U3_gate(0, pi, pi)() ))
        template = 'x q[{}]'.format(indexes)

        Gate.__init__(self, 'X', indexes, gate, template)


class Y_gate(Gate):
    def __init__(self, indexes=None):
        gate = Matrix(simplify(-I * U3_gate(pi / 2, pi, pi/ 2)() ))
        template = 'y q[{}]'.format(indexes)

        Gate.__init__(self, 'Y', indexes, gate, template)


class Z_gate(Gate):
    def __init__(self, indexes=None):
        gate = Matrix(simplify( U1_gate(pi)() ))
        template = 'z q[{}]'.format(indexes)

        Gate.__init__(self, 'Z', indexes, gate, template)


class H_gate(Gate):
    def __init__(self, indexes=None):
        gate = Matrix(simplify(I * U2_gate(0, pi)() ))
        template = 'h q[{}]'.format(indexes)

        Gate.__init__(self, 'H', indexes, gate, template)


class S_gate(Gate):
    def __init__(self, indexes=None):
        gate = Matrix(simplify(U1_gate(pi / 2)() ))
        template = 's q[{}]'.format(indexes)

        Gate.__init__(self, 'S', indexes, gate, template)


class SDG_gate(Gate):
    def __init__(self, indexes=None):
        gate = Matrix(simplify(U1_gate(-pi / 2)() ))
        template = 'sdg q[{}]'.format(indexes)

        Gate.__init__(self, 'SDG', indexes, gate, template)


class T_gate(Gate):
    def __init__(self, indexes=None):
        gate = Matrix(simplify(U1_gate(pi / 4)() ))
        template = 't q[{}]'.format(indexes)

        Gate.__init__(self, 'T', indexes, gate, template)


class TDG_gate(Gate):
    def __init__(self, indexes=None):
        gate = Matrix(simplify(U1_gate(-pi / 4)() ))
        template = 'tdg q[{}]'.format(indexes)

        Gate.__init__(self, 'TDG', indexes, gate, template)


class CX_gate(Gate):
    def __init__(self, indexes=[None, None]):
        gate = gate = Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ])
        template = 'cx q[{}], q[{}]'.format(indexes[0], indexes[1])

        Gate.__init__(self, 'CX', indexes, gate, template)


class CCX_gate(Gate):
    def __init__(self, indexes=[None, None, None]):
        
        # if cx gate restriction is lifted, we can implement 
        # the gate in terms of built in gates
        gate = Matrix([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0],
        ])
        # I = I_gate().gate
        # H = H_gate().gate
        # CX = CX_gate().gate
        # T = T_gate().gate
        # TDG = TDG_gate().gate

        template = 'ccx q[{}], q[{}], q[{}]'.format(
            indexes[0], 
            indexes[1],
            indexes[2])

        Gate.__init__(self, 'CCX', indexes, gate, template)

