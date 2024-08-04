import csv
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def generate_brickwork_circuit_5_qubits():
    qc = QuantumCircuit(5)

    # Define the number of layers in the brickwork pattern
    num_layers = 3

    # Apply the brickwork pattern using a for loop
    for layer in range(num_layers):
        # Apply Hadamard gates to all qubits
        qc.h(range(5))

        # Apply CNOT gates in a staggered fashion
        if layer % 2 == 0:
            # Apply CNOT gates between even-odd pairs
            for i in range(0, 4, 2):
                qc.cx(i, i + 1)
        else:
            # Apply CNOT gates between odd-even pairs
            for i in range(1, 4, 2):
                qc.cx(i, i + 1)

    # Add measurement to all qubits
    qc.measure_all()
    return qc

# Generate two 5-qubit circuits
qc1 = generate_brickwork_circuit_5_qubits()
qc2 = generate_brickwork_circuit_5_qubits()

# Use AerSimulator directly
simulator = AerSimulator()

# Transpile the circuits for the simulator
compiled_circuit1 = transpile(qc1, simulator)
compiled_circuit2 = transpile(qc2, simulator)

# Run the simulations
result1 = simulator.run(compiled_circuit1, shots=1024).result()
result2 = simulator.run(compiled_circuit2, shots=1024).result()

counts1 = result1.get_counts()
counts2 = result2.get_counts()

# Combine the results
def combine_results(counts1, counts2):
    combined_counts = counts1.copy()
    for key, value in counts2.items():
        if key in combined_counts:
            combined_counts[key] += value
        else:
            combined_counts[key] = value
    return combined_counts

combined_counts = combine_results(counts1, counts2)

# Write results to CSV file
def write_counts_to_csv(counts, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Result', 'Count'])  # Header row
        for result, count in counts.items():
            writer.writerow([result, count])

# Path to the output CSV file
csv_file = 'quantum_results.csv'

write_counts_to_csv(combined_counts, csv_file)

# Print and visualize the results
print("Counts for Circuit 1:", counts1)
print("Counts for Circuit 2:", counts2)
print("Combined Counts:", combined_counts)

plot_histogram([counts1, counts2], legend=['Part 1', 'Part 2'])
plot_histogram(combined_counts, title="Combined Results")

