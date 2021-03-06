import functools
from collections import Counter

from sympy import *
from sympy.physics.quantum import TensorProduct, tensor_product_simp, Ket
import numpy as np

import measurements
import gates
import utils


class Barrier(object):
    """Create a barrier in the circuit. 
    
    This prevents optimization of operations across the barrier.
    """

    def __init__(self):
        self.template = 'barrier q'


class Circuit(object):
    """Class for building a quantum circuit.
    """
    
    def __init__(self, num_qubits, num_bits):
        if num_qubits < 1:
            raise ValueError('You must have at least one qubit.')

        self.num_qubits = num_qubits
        self.num_bits = num_bits

        qubits = [Matrix([1,0])] * num_qubits
        self.qubits = utils.tensorproducts(qubits)
        self.bits = [0 for i in range(num_bits)]

        self._measured_bits = None
        self._all_operations = []


    def _is_qubit_available(self, qubit_index):
        if qubit_index > self.num_qubits:
            raise ValueError('Not an available qubit.')


    def _apply_single_gate(self, gate, qubit_index):
        """Apply a single gate by forming the tensor operation.

        If qubit_index is unspecified, apply the gate to all qubits.
        Otherwise, apply the gate to the qubit index.
        """

        if qubit_index is None:
            operator = [gate()] * self.num_qubits
        else:
            self._is_qubit_available(qubit_index)

            operator = [gates.ID_gate()()] * self.num_qubits
            operator[qubit_index] = gate()

        operator = utils.tensorproducts(operator)
        self.qubits = operator * self.qubits
        self._all_operations.append(gate)


    def H(self, qubit_index=None):
        """Apply the Hadamard gate to the qubits."""
        self._apply_single_gate(gates.H_gate(qubit_index), qubit_index)


    def X(self, qubit_index=None):
        """Apply the NOT operation to the qubits."""
        self._apply_single_gate(gates.X_gate(qubit_index), qubit_index)


    def Y(self, qubit_index=None):
        """Apply the Pauli Y operation to the qubits."""
        self._apply_single_gate(gates.Y_gate(qubit_index), qubit_index)


    def Z(self, qubit_index=None):
        """Apply the Pauli Z operation to the qubits."""
        self._apply_single_gate(gates.Z_gate(qubit_index), qubit_index) 


    def ID(self, qubit_index=None):
        """Apply the identity operation to the qubits."""
        self._apply_single_gate(gates.ID_gate(qubit_index), qubit_index)


    def RX(self, theta, qubit_index=None):
        """Apply a rotation gate around the x-axis of the Bloch sphere."""
        self._apply_single_gate(gates.RX_gate(theta, qubit_index), qubit_index)


    def RY(self, theta, qubit_index=None):
        """Apply a rotation gate around the y-axis of the Bloch sphere."""
        self._apply_single_gate(gates.RY_gate(theta, qubit_index), qubit_index)


    def RZ(self, theta, qubit_index=None):
        """Apply a rotation gate around the z-axis of the Bloch sphere."""
        self._apply_single_gate(gates.RZ_gate(theta, qubit_index), qubit_index)


    def U3(self, phi, theta, lambda_, qubit_index=None):
        """Apply the universal gate."""
        self._apply_single_gate(
            gates.U3_gate(phi, theta, lambda_, qubit_index), 
            qubit_index)


    def U2(self, phi, lambda_, qubit_index=None):
        """Apply the U2 gate."""
        self._apply_single_gate(
            gates.U2_gate(phi, lambda_, qubit_index), 
            qubit_index)


    def U1(self, lambda_, qubit_index=None):
        """Apply the universal gate."""
        self._apply_single_gate(
            gates.U1_gate(lambda_, qubit_index), 
            qubit_index)


    def CX(self, control_index, target_index):
        """Flip the target qubit if the control qubit is 1."""

        self._is_qubit_available(control_index)
        self._is_qubit_available(target_index)

        if target_index != control_index + 1:
            raise ValueError('Right now, we can only apply the controlled-X \
                when the target is next to the control qubit.')
        
        operator = [gates.ID_gate()()] * (self.num_qubits - 1)
        cx_gate = gates.CX_gate([control_index, target_index])
        operator[control_index] = cx_gate()
        operator = utils.tensorproducts(operator)

        self.qubits = operator * self.qubits
        self._all_operations.append(cx_gate)


    def CCX(self, control_index1, control_index2, target_index):
        self._is_qubit_available(control_index1)
        self._is_qubit_available(control_index2)
        self._is_qubit_available(target_index)
        
        if (target_index != control_index1 + 2) or \
            (target_index != control_index2 + 1):
            raise ValueError('Right now, we can only apply the CCX \
                when the target is next to the control qubits.')

        operator = [gates.ID_gate()()] * (self.num_qubits - 2)
        cx_gate = gates.CCX_gate([control_index1, control_index2, target_index])
        operator[control_index1] = cx_gate()
        operator = utils.tensorproducts(operator)
        self.qubits = operator * self.qubits
        self._all_operations.append(cx_gate)


    def barrier(self):
        self._all_operations.append(Barrier())


    def reset_qubit(self, qubit_index):
        """Reset a qubit to |0>"""
        raise NotImplementedError


    def execute(self, num_instances):
        """Execute the built circuit a certain number of times.

        Args:
            num_instances (int): number of times to run the circuit

        Returns:
            (dict) mapping possible measured results to number of occurences.
        """
        
        results = [measurements.measure(self.qubits) for i in range(num_instances)]
        return Counter(results)


    def conditional_gate(self):
        """Apply a gate conditioned on a classical bit
        """
        
        raise NotImplementedError


    def compile(self, outfile=None):
        """Compile the built circuit into OpenQASM code.
        """

        with open('templates/header.txt', 'r') as f:
            QASM_file = f.read()

        QASM_file += '\n\nqreg q[{}]\ncreg c[{}]\n\n'.format(
            self.num_qubits, 
            self.num_bits)
        
        for op in self._all_operations:
            QASM_file += op.template + ';\n'
        
        if outfile is not None:
            with open(outfile, 'w+') as f:
                f.write(QASM_file)

        return QASM_file


    def get_state(self, output='bracket'):
        """Returns the resulting qubit state.

        output can be one of:
            `bracket`: linear combination of the computational basis
            `tensor`: tensor product of the state

        Args:
            output (str): output type. 

        Returns:
            sympy Matrix
        """

        if output == 'bracket':
            lin_combin = 0
            qubits = self.qubits
            size = qubits.shape[0]
            num_qubits = int(np.log2(size))

            for i in range(size):
                lin_combin += (qubits[i] * Ket(utils.int_to_binary(i, num_qubits)))

            return lin_combin
        
        elif output == 'tensor':
            return self.qubits

        else:
            raise ValueError('Not a correct output type.')


    def measure(self, qubit_index, bit_index, basis='z'):
        """Perform a measurement under a certain basis.

        Args:
            qubit_index (int): index of measured qubit
            bit_index (int): index of bit to record measured qubit
            basis (str): measurement basis

        Returns:
            None
        """

        if self._measured_bits is None:
            measured_bits = measurements.measure(self.qubits, basis)
            self._measured_bits = measured_bits
            new_state = list(map(
                lambda x: utils.bit_to_matrix(x),
                list(measured_bits)))

            self.qubits = utils.tensorproducts(new_state)

        self.bits[bit_index] = self._measured_bits[-1 * qubit_index - 1]
        self._all_operations.append(measurements.Measure(qubit_index, bit_index))


    def bit_list_to_str(self):
        """Convert the list of bits into a string.
        """
        bits = [str(b) for b in self.bits]
        self.bits = ''.join(bits)