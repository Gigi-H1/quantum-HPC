import pandas as pd
from qiskit import QuantumCircuit, transpile, assemble
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
    """Create a new circuit by copying operations applied to specified qubits."""
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

def simulate_and_save(qc, filename):
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    qobj = assemble(compiled_circuit)
    result = simulator.run(qobj).result()
    counts = result.get_counts(qc)
    counts_df = pd.DataFrame(list(counts.items()), columns=['State', 'Counts'])
    counts_df = counts_df.sort_values(by='Counts', ascending=False)
    counts_df.to_csv(filename, index=False)

# Create the 60-qubit circuit
full_circuit = create_60_qubit_circuit()

# Define qubits for each 30-qubit sub-circuit
qubits_1 = list(range(30))  # First 30 qubits
qubits_2 = list(range(30, 60))  # Last 30 qubits

# Create sub-circuits for 30 qubits
qc1 = create_sub_circuit(full_circuit, qubits_1)
qc2 = create_sub_circuit(full_circuit, qubits_2)

# Simulate each 30-qubit sub-circuit
simulate_and_save(qc1, 'simulation_results_3.csv')
simulate_and_save(qc2, 'simulation_results_4.csv')

print("Simulation results saved to 'simulation_results_3.csv' and 'simulation_results_4.csv'.")

