import csv
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
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
    qc.measure_all()
    return qc

def extract_subcircuit(circuit, start, end):
    # Extract a sub-circuit from the full circuit
    num_qubits = end - start
    sub_circuit = QuantumCircuit(num_qubits)
    
    # Apply gates from the original circuit to the sub-circuit
    for gate in circuit.data:
        if all(q in range(start, end) for q in gate[1]):
            sub_circuit.append(gate[0], [q - start for q in gate[1]])
    
    sub_circuit.measure_all()
    return sub_circuit

def run_simulation(qc, shots=1024):
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator, optimization_level=0)
    
    try:
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts()
        return counts
    except QiskitError as e:
        print(f"Qiskit error during simulation: {e}")
        return None

def combine_counts(counts1, counts2):
    combined_counts = {}
    for key in counts1:
        combined_counts[key] = counts1.get(key, 0)
    for key in counts2:
        combined_counts[key] = combined_counts.get(key, 0) + counts2.get(key, 0)
    return combined_counts

def write_counts_to_csv(counts, filename):
    if counts is None:
        print("No counts available to write to CSV.")
        return
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Result', 'Count'])
        for result, count in counts.items():
            writer.writerow([result, count])

# Generate a 60-qubit brickwork circuit
original_qc = generate_brickwork_circuit(60, 5)

# Extract two 30-qubit sub-circuits
qc1 = extract_subcircuit(original_qc, 0, 30)
qc2 = extract_subcircuit(original_qc, 30, 60)

# Simulate each 30-qubit circuit
counts1 = run_simulation(qc1, shots=1024)
counts2 = run_simulation(qc2, shots=1024)

# Combine the counts from both circuits
combined_counts = combine_counts(counts1, counts2)

# Path to the output CSV file
csv_file = 'quantum_results4.csv'

# Write the results to a CSV file
write_counts_to_csv(combined_counts, csv_file)

# Print the counts
if combined_counts:
    print("Combined Counts:", combined_counts)
else:
    print("No results from simulation.")

