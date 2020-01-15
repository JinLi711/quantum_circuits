# Quantum Circuits

Simulate quantum circuits, compile circuits written in Python into OpenQASM, and visualize the resulting tensorproduct. This repository can be used to understand the basics of quantum operations.

# Installation

First, download this repository and then install the environment using either using [Anaconda](https://anaconda.org/) or [Docker](https://www.docker.com/).

## Using Conda
```
conda create --name quantum_circuits python=3.7
conda activate quantum_circuits
pip install requirements.txt
```

## Using Docker

To build:
```
docker build -t quantum_circuits .
```

To run:
```
docker run -it quantum_circuits bash
```


# Usage

For quick usage:

```
from circuit import Circuit

# build circuit
circ = Circuit(3,5)
circ.X(2)
circ.H()
circ.barrier()

# get the current state of the qubits
circ.get_state()

# execute the circuit 800 times
circ.execute(num_instances=800)

# compile the circuit to OpenQASM
circ.compile()

# perform measurement
circ.measure(0, 1)
```

More examples are located [here](https://github.com/JinLi711/quantum_circuits/blob/master/quantum_circuits/examples.ipynb).


Gates that are currently avaliable are:
* `H`: Hadamard gate
* `ID, X, Y, Z`: Pauli gates
* `RX, RY, RZ`: Rotation gates across (x, y, or z)-axis of the Bloch Sphere
* `U3, U2, U1`: Universal gates
* `S, SDG`: S gate and its transpose
* `T, TDG`: T gate and its transpose
* `CX`: controlled not gate
* `CCX`: Toffoli gate



## Running Tests

To run all the test cases:

```
python tests.py
```

# Caveats
* Circuit gates are implemented niavely (i.e, the operation at a certain time step is created by taking the tensor product of all gates at that time step.) As a result, this implementation is not memory efficient for large numbers of qubits.
* `CX, CCX` gates only work if the control and target qubits are next to each other.
