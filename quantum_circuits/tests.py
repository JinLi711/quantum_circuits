import unittest
import functools

from sympy import *
from sympy.physics.quantum import TensorProduct

import gates
import measurements
import circuit
import utils

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

    # @unittest.skip('Correct')
    def test_U1(self):
        result = gates.U1_gate(self.lambda_)
        result = nsimplify(result)
        U1_gate = Matrix([
            [1, 0.0],
            [0.0, E ** (I * self.lambda_)]
        ])
        self.assertEqual(result, U1_gate)

    # @unittest.skip('Correct')
    def test_RX(self):
        theta = self.theta
        result = gates.RX_gate(theta)
        RX_gate = Matrix([
            [cos(theta / 2.0), -I * sin(theta / 2.0)],
            [-I * sin(theta / 2.0), cos(theta / 2.0)]
        ])
        self.assertEqual(result, RX_gate)

    # @unittest.skip('Correct')
    def test_RY(self):
        theta = self.theta
        result = gates.RY_gate(theta)
        RY_gate = Matrix([
            [cos(theta / 2.0), -sin(theta / 2.0)],
            [sin(theta / 2.0), cos(theta / 2.0)]
        ])
        self.assertEqual(result, RY_gate)

    # @unittest.skip('Correct')
    def test_X(self):
        result = gates.X_gate()
        X_gate = Matrix([
            [0, 1],
            [1, 0]
        ])
        self.assertEqual(result, X_gate)

    # @unittest.skip('Correct')
    def test_H(self):
        result = gates.H_gate()
        H_gate = Matrix([
            [1, 1],
            [1, -1]
        ]) / sqrt(2)
        self.assertEqual(result, H_gate)

    # @unittest.skip('Correct')
    def test_ID(self):
        result = gates.ID_gate()
        ID_gate = Matrix([
            [1, 0],
            [0, 1]
        ])
        self.assertEqual(result, ID_gate)


class test_circuit(unittest.TestCase):

    num_runs = 1000

    @unittest.skip('Correct')
    def test_X(self):
        circ = circuit.Circuit(2, 5)

        state = Matrix([1, 0, 0, 0])
        self.assertEqual(circ.qubits, state)

        circ.X()
        state = Matrix([0, 0, 0, 1])
        self.assertEqual(circ.qubits, state)

        circ = circuit.Circuit(2, 5)
        circ.X(1)
        state = Matrix([0, 1, 0, 0])
        self.assertEqual(circ.qubits, state)

        circ.X(0)
        state = Matrix([0, 0, 0, 1])
        self.assertEqual(circ.qubits, state)

    @unittest.skip('Correct')
    def test_H(self):
        circ = circuit.Circuit(2, 5)
        circ.H()
        state = Matrix([1/2, 1/2, 1/2, 1/2])
        self.assertEqual(circ.qubits, state)

        circ = circuit.Circuit(2, 5)
        circ.H(1)
        state = Matrix([sqrt(2)/ 2, sqrt(2)/ 2, 0, 0])
        self.assertEqual(circ.qubits, state)

    @unittest.skip('Correct')
    def test_CX(self):
        circ = circuit.Circuit(2, 5)
        circ.CX(0, 1)
        state = Matrix([1, 0, 0, 0])
        self.assertEqual(circ.qubits, state)

        circ.X(0)
        circ.CX(0, 1)
        state = Matrix([0, 0, 0, 1])
        self.assertEqual(circ.qubits, state)

    @unittest.skip('Correct')
    def test_execute(self):
        # test deterministic (measuring always produces the same result)
        circ = circuit.Circuit(2, 5)
        circ.X(0)
        results = circ.execute(self.num_runs)
        self.assertEqual(results['10'], self.num_runs)

        # non-deterministic
        # we should have that all possibilities will occur with equal probability
        circ = circuit.Circuit(2, 5)
        circ.H()
        results = circ.execute(self.num_runs)

# @unittest.skip('Still need fixing')
class test_measurements(unittest.TestCase):
    # @unittest.skip('Correct')
    def test_measure(self):
        # tests deterministic measurement
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
        
        state = ['1', '0', '0', '1']
        state = list(map(lambda x: utils.bit_to_matrix(x), state))
        state = utils.tensorproducts(state)
        self.assertEqual(circ.qubits, state)


if __name__ == "__main__":
    unittest.main()