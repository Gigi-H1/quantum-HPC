import argparse
import csv
import os
from qiskit import QuantumCircuit
from qiskit_ibm_provider import IBMProvider
from qiskit.visualization import plot_histogram
from qiskit.compiler import transpile
from qiskit_aer import AerSimulator

def generate_data():
    # Initialize the 60-qubit Quantum Circuit
    qc = QuantumCircuit(60)

    # Define the number of layers in the brickwork pattern
    num_layers = 7

    # Define the gates and angles to be used in the brickwork pattern
    single_qubit_gates = [
        ('h', 0), ('rx', 0.5, 1), ('rz', 1.2, 2), ('ry', 0.3, 3), ('rx', 0.8, 4),
        ('h', 5), ('rx', 1.1, 6), ('rz', 0.9, 7), ('ry', 0.4, 8), ('rx', 0.7, 9),
        ('h', 10), ('rx', 0.6, 11), ('rz', 1.1, 12), ('ry', 0.2, 13), ('rx', 0.9, 14),
        ('h', 15), ('rx', 1.2, 16), ('rz', 0.8, 17), ('ry', 0.5, 18), ('rx', 0.4, 19),
        ('h', 20), ('rx', 0.3, 21), ('rz', 1.4, 22), ('ry', 0.7, 23), ('rx', 0.1, 24),
        ('h', 25), ('rx', 0.5, 26), ('rz', 1.2, 27), ('ry', 0.3, 28), ('rx', 0.8, 29),
        ('h', 30), ('rx', 1.1, 31), ('rz', 0.9, 32), ('ry', 0.4, 33), ('rx', 0.7, 34),
        ('h', 35), ('rx', 0.6, 36), ('rz', 1.1, 37), ('ry', 0.2, 38), ('rx', 0.9, 39),
        ('h', 40), ('rx', 1.2, 41), ('rz', 0.8, 42), ('ry', 0.5, 43), ('rx', 0.4, 44),
        ('h', 45), ('rx', 0.3, 46), ('rz', 1.4, 47), ('ry', 0.7, 48), ('rx', 0.1, 49),
        ('h', 50), ('rx', 0.5, 51), ('rz', 1.2, 52), ('ry', 0.3, 53), ('rx', 0.8, 54),
        ('h', 55), ('rx', 1.1, 56), ('rz', 0.9, 57), ('ry', 0.4, 58), ('rx', 0.7, 59),
    ]

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
                qc.rx(gate[1], gate[2])
            elif gate[0] == 'rz':
                qc.rz(gate[1], gate[2])
            elif gate[0] == 'ry':
                qc.ry(gate[1], gate[2])

        # Apply two-qubit gates in staggered fashion
        if layer % 2 == 0:
            for i in range(len(two_qubit_gates[0])):
                qc.cx(*two_qubit_gates[0][i])
        else:
            for i in range(len(two_qubit_gates[1])):
                qc.cx(*two_qubit_gates[1][i])

    # Apply measurements
    qc.measure_all()

    # Visualize the circuit (optional)
    print(qc.draw())

    return qc

def run_qiskit_simulation(qc):
    # Check available backends
    provider = IBMQ.load_account()
    backends = provider.backends()

    for backend in backends:
        print(f"{backend.name()}: {backend.configuration().n_qubits} qubits")

    # Simulate the circuit using a suitable backend
    simulator = AerSimulator(method='statevector')
    if qc.num_qubits > 33:
        print(f"Warning: Circuit has {qc.num_qubits} qubits, which exceeds the maximum qubit limit of 33.")
        # Consider splitting or optimizing the circuit if needed
        return None

    try:
        compiled_circuit = transpile(qc, simulator)
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
        csv_writer.writerow(['Result', 'Count'])  # Adjust the header according to your data format

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
        print("Simulation failed or the circuit is too large to handle.")

