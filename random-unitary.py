from qiskit.quantum_info import random_unitary
from qiskit import QuantumCircuit
from qiskit.extensions import UnitaryGate

haar_random_gate = UnitaryGate(random_unitary(2))
qc = QuantumCircuit(1)
qc.append(haar_random_gate, [0])
