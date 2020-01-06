from sympy import *
import numpy as np

import utils

def measure(qubits, basis='z'):

    if basis == 'z':

        # compute the tensor product of all the qubit states
        tensor = qubits[0]
        for i in range(1, len(qubits)):
            tensor = Matrix(tensor * qubits[i].T)
        tensor = np.array(tensor)

        # randomly select the measured bits based on the amplitudes
        probabilities = np.absolute(tensor)
        random_choice = np.random.choice(len(tensor), p=probabilities)
        binary_choice = utils.int_to_binary(random_choice, len(tensor))
        return binary_choice

    else:
        raise ValueError('This is not a correct basis measurement.')