from qiskit import*
from qiskit.circuit.library import*
from qiskit_aer import AerSimulator

#simulating quantum circuits using gpu


sim = AerSimulator(method='statevector', device='GPU')

shots = 100
depth = 10
qubits = 25

circuit = transpile(QuantumVolume(qubits, depth, seed=0),backend=sim,optimization_level=0)

circuit.measure_all()

result = execute(circuit, sim, shots=shots, seed_simulator=12345).result()

