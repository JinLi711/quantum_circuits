from sympy import *
import numpy as np

import utils

def measure(qubits, basis='z'):
    """Perform a measurement on the qubits.

    Args:
        qubits (list): list of qubit.Qubit
        basis (str): basis used to measure the qubits

    Returns:
        (str) binary representation of the resulting measurement
    """

    if basis == 'z':

        # compute the tensor product of all the qubit states
        tensor = qubits[0].state
        for i in range(1, len(qubits)):
            tensor = Matrix(flatten(tensor * qubits[i].state.T))
        tensor = np.array(tensor).astype(np.float64)

        # randomly select the measured bits based on the amplitudes
        probabilities = np.absolute(tensor).flatten()
        random_choice = np.random.choice(len(tensor), p=probabilities)
        binary_choice = utils.int_to_binary(random_choice, len(qubits))
        return binary_choice

    else:
        raise ValueError('This is not a correct basis measurement.')