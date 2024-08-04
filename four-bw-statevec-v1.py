import argparse
import csv
import os
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile

def generate_brickwork_circuit():
    # Initialize the 4-qubit Quantum Circuit
    qc = QuantumCircuit(4)

    # Define the number of layers in the brickwork pattern
    num_layers = 2  # Fewer layers for 4 qubits

    # Define the gates and angles to be used in the brickwork pattern
    single_qubit_gates = [
        ('h', 0), ('rx', 0.5, 1), ('rz', 1.2, 2), ('ry', 0.3, 3)
    ]

    two_qubit_gates = [
        [(0, 1), (2, 3)],  # Connections for even layers
        [(1, 2)]           # Connections for odd layers
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

    return qc

def run_qiskit_simulation(qc):
    # Create a simulator with the statevector method
    simulator = AerSimulator(method='statevector', device='GPU')

    # Transpile the circuit
    transpiled_circuit = transpile(qc, simulator, optimization_level=0)

    # Run the simulation
    result = simulator.run(transpiled_circuit).result()
    
    # Get the statevector
    psi = result.get_statevector()

    return psi

def write_statevector_to_csv(statevector, csv_file):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, 'w', newline='') as cf:
        csv_writer = csv.writer(cf)
        csv_writer.writerow(['State Vector'])

        # Write statevector data
        for element in statevector:
            csv_writer.writerow([element])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a 4-qubit brickwork circuit and save the statevector to CSV.")
    parser.add_argument('--csv', required=True, help="Path to the output CSV file.")

    args = parser.parse_args()

    qc = generate_brickwork_circuit()
    statevector = run_qiskit_simulation(qc)
    write_statevector_to_csv(statevector, args.csv)

