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
        qubits = utils.sp_to_np(qubits)
        size = qubits.shape[0]

        # randomly select the measured bits based on the amplitudes
        probabilities = np.absolute(qubits).flatten() ** 2
        random_choice = np.random.choice(size, p=probabilities)
        binary_choice = utils.int_to_binary(random_choice, int(np.log2(size)))
        
        return binary_choice

    else:
        raise ValueError('This is not a correct basis measurement.')