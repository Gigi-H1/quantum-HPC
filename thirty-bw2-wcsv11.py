import argparse
import csv
import os
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile

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
            for gate in two_qubit_gates[0]:
                qc.cx(gate[0], gate[1])
        else:
            for gate in two_qubit_gates[1]:
                qc.cx(gate[0], gate[1])

    # Apply measurements
    qc.measure_all()

    # Visualize the circuit (optional)
    print(qc.draw())

    return qc

def run_qiskit_simulation(qc):
    # For counts (standard simulation)
    simulator_counts = AerSimulator(method='density_matrix', device='GPU')
    transpiled_circuit_counts = transpile(qc, simulator_counts, optimization_level=0)  # Avoid backend constraints
    result_counts = simulator_counts.run(transpiled_circuit_counts, shots=20000).result()
    counts = result_counts.get_counts(transpiled_circuit_counts)

    # For statevector (no measurements)
    qc_no_measure = qc.remove_final_measurements(inplace=False)
    simulator_statevector = AerSimulator(method='statevector', device='GPU')
    transpiled_circuit_statevector = transpile(qc_no_measure, simulator_statevector, optimization_level=0)  # Avoid backend constraints
    result_statevector = simulator_statevector.run(transpiled_circuit_statevector).result()
    psi = result_statevector.get_statevector(transpiled_circuit_statevector, decimals=3)

    return counts, psi

def write_data_to_csv(counts, psi, csv_file):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, 'w', newline='') as cf:
        csv_writer = csv.writer(cf)
        csv_writer.writerow(['Result', 'Count', 'State Vector'])

        # Write counts data
        for key, value in counts.items():
            csv_writer.writerow([key, value, ''])

        # Write statevector data
        csv_writer.writerow(['', '', ''])
        csv_writer.writerow(['State Vector', '', ''])
        for vector in psi:
            csv_writer.writerow(['', '', vector])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate data and save to CSV.")
    parser.add_argument('--csv', required=True, help="Path to the output CSV file.")

    args = parser.parse_args()

    qc = generate_data()
    counts, psi = run_qiskit_simulation(qc)
    write_data_to_csv(counts, psi, args.csv)

