import pandas as pd
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import AerSimulator

def create_60_qubit_circuit():
    qc = QuantumCircuit(60)
    # Example operations on the 60-qubit circuit
    for i in range(30):
        qc.h(i)  # Apply Hadamard gates on the first 30 qubits
    for i in range(30, 60):
        qc.cx(i - 30, i)  # Apply CNOT gates on the last 30 qubits
    qc.measure_all()
    return qc

def create_sub_circuit(full_circuit, qubits):
    """Creates a new quantum circuit with the specified qubits."""
    sub_circuit = QuantumCircuit(len(qubits))
    for qubit in qubits:
        sub_circuit.append(full_circuit.data[qubit], qubits)
    sub_circuit.measure_all()
    return sub_circuit

def simulate_and_save(qc, filename):
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    qobj = assemble(compiled_circuit)
    result = simulator.run(qobj).result()
    counts = result.get_counts(qc)
    counts_df = pd.DataFrame(list(counts.items()), columns=['State', 'Counts'])
    counts_df = counts_df.sort_values(by='Counts', ascending=False)
    counts_df.to_csv(filename, index=False)

# Create the 60-qubit circuit
full_circuit = create_60_qubit_circuit()

# Define qubits for each 30-qubit sub-circuit
qubits_1 = list(range(30))  # First 30 qubits
qubits_2 = list(range(30, 60))  # Last 30 qubits

# Create sub-circuits for 30 qubits
qc1 = create_sub_circuit(full_circuit, qubits_1)
qc2 = create_sub_circuit(full_circuit, qubits_2)

# Simulate each 30-qubit sub-circuit
simulate_and_save(qc1, 'simulation_results_1.csv')
simulate_and_save(qc2, 'simulation_results_2.csv')

print("Simulation results saved to 'simulation_results_1.csv' and 'simulation_results_2.csv'.")

