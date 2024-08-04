import csv
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
    """Create a new circuit with specified qubits and their operations."""
    sub_circuit = QuantumCircuit(len(qubits))
    # Map original qubits to the sub-circuit qubits
    qubit_mapping = {original: new for new, original in enumerate(qubits)}
    for operation, qargs, cargs in full_circuit.data:
        mapped_qargs = [qubit_mapping.get(qarg, None) for qarg in qargs]
        # Skip operations involving qubits not in this sub-circuit
        if None not in mapped_qargs:
            sub_circuit.append(operation, mapped_qargs)
    sub_circuit.measure_all()
    return sub_circuit

def simulate_and_save(qc, filename):
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    qobj = assemble(compiled_circuit)
    result = simulator.run(qobj).result()
    counts = result.get_counts(qc)

    # Write results to a CSV file manually
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['State', 'Counts'])
        for state, count in counts.items():
            csvwriter.writerow([state, count])

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

