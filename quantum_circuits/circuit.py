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
        self.bits = [0 for i in range(num_qubits)]


    def get_qubit(self, qubit_index):
        return self.qubits[qubit_index]

    def H(self, qubit_index):
        self.get_qubit(qubit_index).H

    def X(self, qubit_index):
        self.get_qubit(qubit_index).X

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
        """Returns the resulting tensorproduct superposition.
        """

        pass

    def measure(self, qubit_index, bit_index, basis='z'):
        measured_bits = measure(self.qubits, basis)
        self.bits[bit_index] = measured_bits[qubit_index]