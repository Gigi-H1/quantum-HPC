import csv
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.exceptions import QiskitError

def generate_brickwork_circuit(num_qubits, num_layers):
    qc = QuantumCircuit(num_qubits)
    for layer in range(num_layers):
        qc.h(range(num_qubits))
        if layer % 2 == 0:
            for i in range(0, num_qubits - 1, 2):
                qc.cx(i, i + 1)
        else:
            for i in range(1, num_qubits - 1, 2):
                qc.cx(i, i + 1)
    return qc

def combine_circuits(circuit1, circuit2):
    num_qubits1 = circuit1.num_qubits
    num_qubits2 = circuit2.num_qubits
    combined_circuit = QuantumCircuit(num_qubits1 + num_qubits2)
    combined_circuit.compose(circuit1, qubits=range(num_qubits1), inplace=True)
    combined_circuit.compose(circuit2, qubits=range(num_qubits1, num_qubits1 + num_qubits2), inplace=True)
    return combined_circuit

def run_simulation_and_get_counts(qc, shots=1024):
    try:
        simulator = AerSimulator()
        # Define a coupling map for 60 qubits (fully connected)
        coupling_map = [[i, j] for i in range(60) for j in range(i+1, 60)]
        compiled_circuit = transpile(qc, simulator, optimization_level=0, coupling_map=coupling_map)
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts()
        return counts
    except QiskitError as e:
        print(f"Qiskit error during simulation: {e}")
        return None

def write_counts_to_csv(counts, filename):
    if counts is None:
        print("No counts available to write to CSV.")
        return
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Result', 'Count'])
        for result, count in counts.items():
            writer.writerow([result, count])

# Generate two 30-qubit circuits
qc1 = generate_brickwork_circuit(30, 5)
qc2 = generate_brickwork_circuit(30, 5)

# Combine the circuits into a single 60-qubit circuit
combined_qc = combine_circuits(qc1, qc2)

# Run the simulation
combined_counts = run_simulation_and_get_counts(combined_qc, shots=1024)

# Path to the output CSV file
csv_file = 'quantum_results4.csv'

# Write the results to a CSV file
write_counts_to_csv(combined_counts, csv_file)

# Print the counts and visualize the results if available
if combined_counts:
    print("Combined Counts:", combined_counts)
    plot_histogram(combined_counts, title="Combined 60-Qubit Brickwork Circuit Results")
else:
    print("No results from simulation.")

