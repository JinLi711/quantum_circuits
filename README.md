# Quantum Circuits
Compile circuits written in Python into OpenQASM code and visualize the resulting tensorproduct. This repository is mainly used for educational purposes.

# Installation

First, download this repository and install either using [Anaconda](https://anaconda.org/) or [Docker](https://www.docker.com/)

## Using Conda
```
conda create --name quantum_circuits python=3.7
conda activate quantum_circuits
pip install requirements.txt
```

## Using Docker


# Usage

For quick usage:

```
circ = Circuit(3,5)
```

Gates that are currently avaliable are:
* `H`: Hadamard
* `X`: Pauli X
* `ID`: Identity 
* `RX, RY, RZ`: Rotation across (x, y, or z)-axis of the Bloch Sphere
* `U3, U2, U1`: Universal Gates
* `CX`: controlled not gate

## Examples

Examples are located [here](https://github.com/JinLi711/quantum_circuits/examples/examples.ipynb)

## Running Tests

To run all the test cases:

```
python tests.py
```

# Notes
* The not meant to handle large numbers of qubits.
* When applying gates, either the same gate is applied to all qubits or that gate is applied to a single qubit.
* Right now, we can only create a single quantum register.