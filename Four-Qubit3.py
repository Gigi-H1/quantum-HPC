from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Initialize the 4-qubit Quantum Circuit
qc = QuantumCircuit(4)

# Define the number of layers in the brickwork pattern
num_layers = 3

# Define the gates and angles to be used in the brickwork pattern
single_qubit_gates = [
    ('h', 0), ('rx', 0.5, 1), ('rz', 1.2, 2), ('ry', 0.3, 3)
]
two_qubit_gates = [
    (0, 1), (1, 2), (2, 3), (3, 0)
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
        for i in range(0, len(two_qubit_gates), 2):
            qc.cx(two_qubit_gates[i][0], two_qubit_gates[i][1])
    else:
        for i in range(1, len(two_qubit_gates), 2):
            qc.cx(two_qubit_gates[i][0], two_qubit_gates[i][1])

# Apply measurements
qc.measure_all()

# Visualize the circuit
print(qc.draw())

# Transpile the circuit for the simulator


# Simulate the circuit using qiskit-aer-gpu
simulator = AerSimulator(method='statevector', device='GPU')
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit, shots=1024).result()
counts = result.get_counts(compiled_circuit)


# Plot the results
plot_histogram(counts)
