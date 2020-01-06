import functools

from sympy import *
from sympy.physics.quantum import TensorProduct, tensor_product_simp

from qubit import Qubit
from measurements import measure

class Circuit(object):
    """Class for building a quantum circuit.
    """
    
    def __init__(self, num_qubits, num_bits):
        if num_qubits < 1:
            raise ValueError('You must have at least one qubit.')

        self.num_qubits = num_qubits
        self.num_bits = num_bits
        self.qubits = [Qubit(i) for i in range(num_qubits)]
        self.bits = [0 for i in range(num_bits)]
        self._measured_bits = None


    def get_qubit(self, qubit_index):
        return self.qubits[qubit_index]

    def H(self, qubit_index):
        self.get_qubit(qubit_index).H()

    def X(self, qubit_index):
        self.get_qubit(qubit_index).X()

    def CX(self, control_index, target_index):
        # TODO: implement this
        pass

    def execute(self, num_instances):
        """Execute the built circuit a certain number of times.

        Args:
            num_instances (int): number of times to run the circuit

        Returns:
            (dict) mapping possible measured results to number of occurences.
        """
        pass

    def compile(self):
        """Compile the built circuit into OpenQASM code.
        """

        pass

    def tensor_syntax(self):
        """Returns the resulting tensorproduct superposition in Sympy syntax.
        """

        tensor = self.qubits[0].state
        for i in range(1, self.num_qubits):
            tensor = TensorProduct(tensor, self.qubits[i].state)

        tensor = tensor_product_simp(tensor)
        return tensor

    def measure(self, qubit_index, bit_index, basis='z'):
        """Perform a measurement under a certain basis.
        """

        if self._measured_bits is None:
            measured_bits = measure(self.qubits, basis)
            self._measured_bits = measured_bits
            for i, bit in enumerate(measured_bits):
                self.qubits[i].reset_state()

                if bit == '1':
                    self.qubits[i].X()

        self.bits[bit_index] = self._measured_bits[-1 * qubit_index - 1]


    def bit_list_to_str(self):
        """Convert the list of bits into a string.
        """
        bits = [str(b) for b in self.bits]
        self.bits = ''.join(bits)