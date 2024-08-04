from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

def generate_and_split_circuit():
    qc = QuantumCircuit(60)

    # Apply some gates to the first 30 qubits
    for i in range(30):
        qc.h(i)
    
    # Apply some gates to the second 30 qubits
    for i in range(30, 60):
        qc.h(i)
    
    # Add some two-qubit gates between different parts of the circuit
    for i in range(30):
        qc.cx(i, i + 30)
    
    qc.measure_all()
    return qc

def split_into_subcircuits(qc):
    # Extract two sub-circuits from the original circuit
    qc1 = qc.copy().truncate(start=0, end=30)
    qc2 = qc.copy().truncate(start=30, end=60)
    
    return qc1, qc2

def run_qiskit_simulation(qc):
    simulator = AerSimulator(method='statevector')
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit).result()
    statevector = result.get_statevector()
    return statevector

def combine_results(statevector1, statevector2):
    # Combine statevectors from both sub-circuits
    combined_statevector = np.kron(statevector1, statevector2)
    return combined_statevector

# Main
qc = generate_and_split_circuit()
qc1, qc2 = split_into_subcircuits(qc)

statevector1 = run_qiskit_simulation(qc1)
statevector2 = run_qiskit_simulation(qc2)

combined_statevector = combine_results(statevector1, statevector2)

print("Combined Statevector:", combined_statevector)

