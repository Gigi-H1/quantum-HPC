import argparse
import csv
import os
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def generate_data_partition(partition):
    # Initialize a Quantum Circuit for the partition
    qc = QuantumCircuit(30)

    # Define the number of layers in the brickwork pattern
    num_layers = 7

    # Define the single-qubit gates with angles and their respective qubit indices
    single_qubit_gates = [
        ('h', 0), ('rx', 1, 0.5), ('rz', 2, 1.2), ('ry', 3, 0.3), ('rx', 4, 0.8),
        ('h', 5), ('rx', 6, 1.1), ('rz', 7, 0.9), ('ry', 8, 0.4), ('rx', 9, 0.7),
        ('h', 10), ('rx', 11, 0.6), ('rz', 12, 1.1), ('ry', 13, 0.2), ('rx', 14, 0.9),
        ('h', 15), ('rx', 16, 1.2), ('rz', 17, 0.8), ('ry', 18, 0.5), ('rx', 19, 0.4),
        ('h', 20), ('rx', 21, 0.3), ('rz', 22, 1.4), ('ry', 23, 0.7), ('rx', 24, 0.1),
        ('h', 25), ('rx', 26, 0.5), ('rz', 27, 1.2), ('ry', 28, 0.3), ('rx', 29, 0.8)
    ]

    # Two-qubit gates for the partition
    two_qubit_gates = [
        [(i, i+1) for i in range(0, 30, 2)], [(i, i+1) for i in range(1, 29, 2)]
    ]

    # Apply the brickwork pattern using a for loop
    for layer in range(num_layers):
        # Apply single-qubit gates
        for gate in single_qubit_gates:
            if gate[0] == 'h':
                qc.h(gate[1])
            elif gate[0] == 'rx':
                qc.rx(gate[2], gate[1])
            elif gate[0] == 'rz':
                qc.rz(gate[2], gate[1])
            elif gate[0] == 'ry':
                qc.ry(gate[2], gate[1])

        # Apply two-qubit gates in staggered fashion
        for q1, q2 in two_qubit_gates[layer % 2]:
            qc.cx(q1, q2)

    # Apply measurements
    qc.measure_all()

    return qc

def run_qiskit_simulation(qc):
    # Use Qiskit's Aer simulator for local simulation
    simulator = AerSimulator()

    # Transpile the circuit for the simulator
    compiled_circuit = transpile(qc, simulator)


    # Run the simulation
    result = simulator.run(compiled_circuit, shots=1000000).result()
    counts = result.get_counts(compiled_circuit)
    return counts
    

def merge_counts(counts1, counts2):
    # Merge the counts from two simulations
    merged_counts = counts1.copy()
    for key, value in counts2.items():
        if key in merged_counts:
            merged_counts[key] += value
        else:
            merged_counts[key] = value
    return merged_counts

def write_data_to_csv(data, csv_file):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, 'w', newline='') as cf:
        csv_writer = csv.writer(cf)
        csv_writer.writerow(['Result', 'Count'])

        for key, value in data.items():
            csv_writer.writerow([key, value])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate data and save to CSV.")
    parser.add_argument('--csv', required=True, help="Path to the output CSV file.")

    args = parser.parse_args()

    # Generate data for each partition
    qc_partition1 = generate_data_partition(partition=1)
    qc_partition2 = generate_data_partition(partition=2)

    # Run the simulation for each partition
    counts_partition1 = run_qiskit_simulation(qc_partition1)
    counts_partition2 = run_qiskit_simulation(qc_partition2)

    # Merge the counts from both partitions
    if counts_partition1 and counts_partition2:
        merged_counts = merge_counts(counts_partition1, counts_partition2)
        write_data_to_csv(merged_counts, args.csv)
    else:
        print("Simulation failed for one or both partitions.")

