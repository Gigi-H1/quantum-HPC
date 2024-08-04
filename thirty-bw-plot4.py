import random
import argparse
import csv
import os
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

def generate_data():
    # Initialize the 30-qubit Quantum Circuit
    qc = QuantumCircuit(30)

    # Define the number of layers in the brickwork pattern
    num_layers = 7

    # Define the gates and angles to be used in the brickwork pattern
    single_qubit_gates = [
        ('h', 0), ('rx', 0.5, 1), ('rz', 1.2, 2), ('ry', 0.3, 3), ('rx', 0.8, 4),
        ('h', 5), ('rx', 1.1, 6), ('rz', 0.9, 7), ('ry', 0.4, 8), ('rx', 0.7, 9),
        ('h', 10), ('rx', 0.6, 11), ('rz', 1.1, 12), ('ry', 0.2, 13), ('rx', 0.9, 14),
        ('h', 15), ('rx', 1.2, 16), ('rz', 0.8, 17), ('ry', 0.5, 18), ('rx', 0.4, 19),
        ('h', 20), ('rx', 0.3, 21), ('rz', 1.4, 22), ('ry', 0.7, 28), ('rx', 0.1, 29)
    ]

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
                qc.rx(gate[1], gate[2])
            elif gate[0] == 'rz':
                qc.rz(gate[1], gate[2])
            elif gate[0] == 'ry':
                qc.ry(gate[1], gate[2])

        # Apply two-qubit gates in staggered fashion
        if layer % 2 == 0:
            # Even layers: Use the first list in two_qubit_gates
            for (q1, q2) in two_qubit_gates[0]:
                qc.cx(q1, q2)
        else:
            # Odd layers: Use the second list in two_qubit_gates
            for (q1, q2) in two_qubit_gates[1]:
                qc.cx(q1, q2)

    # Apply measurements
    qc.measure_all()

    return qc

def run_qiskit_simulation(qc):
    # Simulate the circuit using qiskit-aer-gpu
    simulator = AerSimulator(method='statevector', device='GPU')
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=10000)
    result = job.result()
    counts = result.get_counts()

    real_parts = result.data()['statevector'].real
    imag_parts = result.data()['statevector'].imag

    # Plot the statevector waveform
    plt.figure(figsize=(12, 6))
    plt.plot(real_parts, label='Real Part')
    plt.plot(imag_parts, label='Imaginary Part')
    plt.title('Statevector Waveform')
    plt.xlabel('Basis State Index')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

    # Extract and plot probability distribution as waveform
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    sorted_states = sorted(probabilities.keys())
    probability_values = [probabilities[state] for state in sorted_states]

    plt.figure(figsize=(12, 6))
    plt.plot(sorted_states, probability_values, marker='o')
    plt.title('Probability Distribution Waveform')
    plt.xlabel('Measured State')
    plt.ylabel('Probability')
    plt.xticks(rotation=90)  # Rotate state labels for better readability
    plt.show()

    # Visualize the circuit (optional)
    print(qc.draw())
    plot_histogram(counts)
    plt.show()
    return counts

def write_data_to_csv(data, csv_file):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, 'w', newline='') as cf:
        csv_writer = csv.writer(cf)
        csv_writer.writerow(['Result', 'Count'])  # Adjust the header according to your data format

        for key, value in data.items():
            csv_writer.writerow([key, value])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate data and save to CSV.")
    parser.add_argument('--csv', required=True, help="Path to the output CSV file.")

    args = parser.parse_args()

    qc = generate_data()
    counts = run_qiskit_simulation(qc)
    write_data_to_csv(counts, args.csv)

