import argparse
import csv
import os
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def generate_data():
    # Initialize the 60-qubit Quantum Circuit
    qc = QuantumCircuit(60)

    # Define the number of layers in the brickwork pattern
    num_layers = 7

    # Define the single-qubit gates with angles
    single_qubit_gates = [
        ('h', 0), ('rx', 1, 0.5), ('rz', 2, 1.2), ('ry', 3, 0.3), ('rx', 4, 0.8),
        ('h', 5), ('rx', 6, 1.1), ('rz', 7, 0.9), ('ry', 8, 0.4), ('rx', 9, 0.7),
        ('h', 10), ('rx', 11, 0.6), ('rz', 12, 1.1), ('ry', 13, 0.2), ('rx', 14, 0.9),
        ('h', 15), ('rx', 16, 1.2), ('rz', 17, 0.8), ('ry', 18, 0.5), ('rx', 19, 0.4),
        ('h', 20), ('rx', 21, 0.3), ('rz', 22, 1.4), ('ry', 23, 0.7), ('rx', 24, 0.1),
        ('h', 25), ('rx', 26, 0.5), ('rz', 27, 1.2), ('ry', 28, 0.3), ('rx', 29, 0.8),
        ('h', 30), ('rx', 31, 1.1), ('rz', 32, 0.9), ('ry', 33, 0.4), ('rx', 34, 0.7),
        ('h', 35), ('rx', 36, 0.6), ('rz', 37, 1.1), ('ry', 38, 0.2), ('rx', 39, 0.9),
        ('h', 40), ('rx', 41, 1.2), ('rz', 42, 0.8), ('ry', 43, 0.5), ('rx', 44, 0.4),
        ('h', 45), ('rx', 46, 0.3), ('rz', 47, 1.4), ('ry', 48, 0.7), ('rx', 49, 0.1),
        ('h', 50), ('rx', 51, 0.5), ('rz', 52, 1.2), ('ry', 53, 0.3), ('rx', 54, 0.8),
        ('h', 55), ('rx', 56, 1.1), ('rz', 57, 0.9), ('ry', 58, 0.4), ('rx', 59, 0.7)]

    # Define the two-qubit gate pairs for each layer
    two_qubit_gates = [
        [(i, i+1) for i in range(0, 60, 2)], [(i, i+1) for i in range(1, 59, 2)]
    ]

    # Apply the brickwork pattern using a for loop
    for layer in range(num_layers):
        # Apply single-qubit gates
        for gate in single_qubit_gates:
            if gate[0] == 'h':
                qc.h(gate[1])
            elif gate[0] == 'rx':
                qc.rx(gate[2], gate[1])  # Corrected order: angle, qubit index
            elif gate[0] == 'rz':
                qc.rz(gate[2], gate[1])  # Corrected order: angle, qubit index
            elif gate[0] == 'ry':
                qc.ry(gate[2], gate[1])  # Corrected order: angle, qubit index

        # Apply two-qubit gates in staggered fashion
        for q1, q2 in two_qubit_gates[layer % 2]:
            qc.cx(q1, q2)

    # Apply measurements
    qc.measure_all()

    # Visualize the circuit (optional)
    print(qc.draw())

    return qc

def run_qiskit_simulation(qc):
    # Use Qiskit's Aer simulator for local simulation
    simulator = AerSimulator()

    # Transpile the circuit for the simulator
    compiled_circuit = transpile(qc, simulator)

    try:
        # Run the simulation
        result = simulator.run(compiled_circuit, shots=1000000).result()
        counts = result.get_counts(compiled_circuit)
        return counts
    except Exception as e:
        print(f"Error during simulation: {e}")
        return None

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

    qc = generate_data()
    counts = run_qiskit_simulation(qc)
    if counts:
        write_data_to_csv(counts, args.csv)
    else:
        print("Simulation failed.")

