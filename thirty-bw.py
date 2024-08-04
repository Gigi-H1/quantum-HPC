import numpy as np
from qiskit import QuantumCircuit, transpile, execute, Aer
from qiskit.visualization import plot_histogram

# Initialize the 30-qubit Quantum Circuit
qc = QuantumCircuit(30)

# Define the number of layers in the brickwork pattern
num_layers = 7

# Function to generate random angles
def random_angle():
    return np.random.uniform(0, 2 * np.pi)

# Define the single-qubit gates and their random angles
single_qubit_gates = [
    ('h', 0), ('rx', random_angle(), 1), ('rz', random_angle(), 2), ('ry', random_angle(), 3), ('rx', random_angle(), 4),
    ('h', 5), ('rx', random_angle(), 6), ('rz', random_angle(), 7), ('ry', random_angle(), 8), ('rx', random_angle(), 9),
    ('h', 10), ('rx', random_angle(), 11), ('rz', random_angle(), 12), ('ry', random_angle(), 13), ('rx', random_angle(), 14),
    ('h', 15), ('rx', random_angle(), 16), ('rz', random_angle(), 17), ('ry', random_angle(), 18), ('rx', random_angle(), 19),
    ('h', 20), ('rx', random_angle(), 21), ('rz', random_angle(), 22), ('ry', random_angle(), 23), ('rx', random_angle(), 24),
    ('h', 25), ('rx', random_angle(), 26), ('rz', random_angle(), 27), ('ry', random_angle(), 28), ('rx', random_angle(), 29)
]

# Define two-qubit gates for brickwork pattern
# Define layer connections
two_qubit_gates_layers = [
    [(i, i+1) for i in range(0, 30, 2)],  # Connections for even layers
    [(i, i+1) for i in range(1, 29, 2)]   # Connections for odd layers
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
    two_qubit_gates = two_qubit_gates_layers[layer % 2]
    for qubit_pair in two_qubit_gates:
        qc.cx(qubit_pair[0], qubit_pair[1])

# Apply measurements
qc.measure_all()

# Visualize the circuit
print(qc.draw())

# Simulate the circuit
backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1024).result()
counts = result.get_counts(qc)

# Plot the results
plot_histogram(counts)

