import pandas as pd
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import AerSimulator

def create_60_qubit_circuit():
    qc = QuantumCircuit(60)
    # Example operations on all qubits
    for i in range(30):
        qc.h(i)  # Apply Hadamard gates on the first 30 qubits
    for i in range(30, 60):
        qc.cx(i - 30, i)  # Apply CNOT gates on the last 30 qubits
    qc.measure_all()
    return qc

def split_circuit(circuit):
    # Create two 30-qubit circuits from the 60-qubit circuit
    qc1 = circuit[:30]
    qc2 = circuit[30:]
    return qc1, qc2

def simulate_and_save(qc, filename):
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    qobj = assemble(compiled_circuit)
    result = simulator.run(qobj).result()
    counts = result.get_counts(qc)
    counts_df = pd.DataFrame(list(counts.items()), columns=['State', 'Counts'])
    counts_df = counts_df.sort_values(by='Counts', ascending=False)
    counts_df.to_csv(filename, index=False)

# Create and split the 60-qubit circuit
full_circuit = create_60_qubit_circuit()
qc1, qc2 = split_circuit(full_circuit)

# Simulate each 30-qubit circuit
simulate_and_save(qc1, 'simulation_results_1.csv')
simulate_and_save(qc2, 'simulation_results_2.csv')

print("Simulation results saved to 'simulation_results_1.csv' and 'simulation_results_2.csv'.")

