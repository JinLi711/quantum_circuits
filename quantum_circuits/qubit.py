from sympy import *

import gates

class Qubit(object):

    def __init__(self, qubit_position):
        self.qubit_position = qubit_position
        self.reset_state()

    def reset_state(self):
        self.state = Matrix([1, 0])

    def H(self):  
        self.state = gates.H_gate() * self.state

    def X(self):   
        self.state = gates.X_gate() * self.state
