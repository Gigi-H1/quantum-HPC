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
    # Create empty circuits for the two 30-qubit sections
    qc1 = QuantumCircuit(30)
    qc2 = QuantumCircuit(30)
    
    # Copy operations from the first half of the original circuit
    for instr, qargs, cargs in qc.data:
        if all(q < 30 for q in qargs):
            qc1.append(instr, qargs)
    
    # Copy operations from the second half of the original circuit
    for instr, qargs, cargs in qc.data:
        if all(q >= 30 for q in qargs):
            new_qargs = [q - 30 for q in qargs]
            qc2.append(instr, new_qargs)
    
    return qc1, qc2

def run_qiskit_simulation(qc):
    # Use Qiskit's Aer simulator for local simulation
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

