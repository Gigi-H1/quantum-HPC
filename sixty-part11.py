import pandas as pd
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer

# Create a quantum circuit
qc = QuantumCircuit(2)
qc.h(0)      # Apply Hadamard gate to qubit 0
qc.cx(0, 1)  # Apply CNOT gate with qubit 0 as control and qubit 1 as target
qc.measure_all()  # Measure all qubits

# Set up the simulator
simulator = Aer.get_backend('aer_simulator')

# Compile and assemble the circuit
compiled_circuit = transpile(qc, simulator)
qobj = assemble(compiled_circuit)

# Run the simulation
result = simulator.run(qobj).result()

# Get counts from the result
counts = result.get_counts(qc)

# Convert counts to a DataFrame
counts_df = pd.DataFrame(list(counts.items()), columns=['State', 'Counts'])

# Optional: sort the DataFrame by counts in descending order
counts_df = counts_df.sort_values(by='Counts', ascending=False)

# Save the DataFrame to a CSV file
counts_df.to_csv('simulation_resultss.csv', index=False)

print("Results have been saved to 'simulation_results.csv'.")

