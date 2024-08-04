from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city

# Initialize the 4-qubit Quantum Circuit
qc = QuantumCircuit(30)

# Define the number of layers in the brickwork pattern
num_layers = 7

# Define the gates and angles to be used in the brickwork pattern
single_qubit_gates = [
    ('h', 0), ('rx', 0.5, 1), ('rz', 1.2, 2), ('ry', 0.3, 3),('rx',0.8, 4), ('h', 5), ('rx', 1.1, 6), ('rz', 0.9, 7), ('ry', 0.4, 8), ('rx', 0.7, 9), ('h', 10), ('rx', 0.6, 11), ('rz', 1.1, 12), ('ry', 0.2, 13), ('rx', 0.9, 14), ('h', 15), ('rx', 1.2, 16), ('rz', 0.8, 17), ('ry', 0.5, 18), ('rx', 0.4, 19), ('h', 20), ('rx', 0.3, 21), ('rz', 1.4, 22), ('ry', 0.7, 28), ('rx', 0.1, 29)
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
        for i in range(0, len(two_qubit_gates), 2):
            qc.cx(two_qubit_gates[i][0], two_qubit_gates[i][1])
    else:
        for i in range(1, len(two_qubit_gates), 2):
            qc.cx(two_qubit_gates[i][0], two_qubit_gates[i][1])

# Apply measurements
qc.measure_all()

# Visualize the circuit
print(qc.draw())

simulator = AerSimulator(method='statevector', device='GPU')
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit).result()
statevector = result.get_statevector(compiled_circuit)


print("Statevector:", statevector)

plot_state_city(statevector).show()

# Plot the results
#plot_histogram(counts)


