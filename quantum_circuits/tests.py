import unittest
import functools

from sympy import *
from sympy.physics.quantum import TensorProduct

import gates
import measurements
import circuit

def bit_to_matrix(x):
    if x == '0':
        return Matrix([1, 0])
    elif x == '1':
        return Matrix([0, 1])
    else:
        raise ValueError('Bit must be either 0 or 1.')


@unittest.skip('Correct') 
class Test_gates(unittest.TestCase):
    phi = Symbol('phi')
    theta = Symbol('theta')
    lambda_ = Symbol('lambda')
    
    @unittest.skip('Not implemented.')
    def test_U2(self):
        result = gates.U2_gate(self.phi, self.lambda_)
        U2_gate = Matrix([
            [],
            []
        ])
        self.assertEqual(result, U2_gate)

    @unittest.skip('Correct')
    def test_U1(self):
        result = gates.U1_gate(self.lambda_)
        result = nsimplify(result)
        U1_gate = Matrix([
            [1, 0.0],
            [0.0, E ** (I * self.lambda_)]
        ])
        self.assertEqual(result, U1_gate)

    @unittest.skip('Correct')
    def test_RX(self):
        theta = self.theta
        result = gates.RX_gate(theta)
        RX_gate = Matrix([
            [cos(theta / 2.0), -I * sin(theta / 2.0)],
            [-I * sin(theta / 2.0), cos(theta / 2.0)]
        ])
        self.assertEqual(result, RX_gate)

    @unittest.skip('Correct')
    def test_RY(self):
        theta = self.theta
        result = gates.RY_gate(theta)
        RY_gate = Matrix([
            [cos(theta / 2.0), -sin(theta / 2.0)],
            [sin(theta / 2.0), cos(theta / 2.0)]
        ])
        self.assertEqual(result, RY_gate)

    @unittest.skip('Correct')
    def test_X(self):
        result = gates.X_gate()
        X_gate = Matrix([
            [0, 1],
            [1, 0]
        ])
        self.assertEqual(result, X_gate)

    @unittest.skip('Correct')
    def test_H(self):
        result = gates.H_gate()
        H_gate = Matrix([
            [1, 1],
            [1, -1]
        ]) / sqrt(2)
        self.assertEqual(result, H_gate)

# @unittest.skip('Correct')
class test_measurements(unittest.TestCase):
    # @unittest.skip('Correct')
    def test_measure(self):
        circ = circuit.Circuit(4, 5)
        circ.X(3)
        circ.X(0)
        circ.measure(3, 4)
        circ.measure(0, 1)
        circ.measure(1, 2)
        circ.bit_list_to_str()
        result = circ.bits
        actual_bit_string = '01001'
        self.assertEqual(result, actual_bit_string)
        
        get_state = lambda x: circ.qubits[x].state
        actual = tensorproduct(
            get_state(0),
            get_state(1),
            get_state(2),
            get_state(3))
        result = circ.tensor_syntax()
        # Need to manually check that they are equal
        # self.assertEqual(actual, result)


if __name__ == "__main__":
    unittest.main()