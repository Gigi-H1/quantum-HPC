from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit_aer import Aer
import csv

def generate_60_qubit_circuit():
    num_qubits = 60
    num_layers = 5  # Number of layers in the brickwork pattern
    qc = QuantumCircuit(num_qubits)
    
    for layer in range(num_layers):
        # Apply single-qubit gates (example: Hadamard gates)
        qc.h(range(num_qubits))
        
        # Apply two-qubit gates in a brickwork pattern
        if layer % 2 == 0:
            for i in range(0, num_qubits - 1, 2):
                qc.cx(i, i + 1)
        else:
            for i in range(1, num_qubits - 1, 2):
                qc.cx(i, i + 1)
    
    qc.measure_all()
    return qc

def run_simulation(qc, shots=1024):
    # Use the AerSimulator for local simulation
    simulator = Aer.get_backend('aer_simulator')
    
    # Transpile the circuit for the simulator
    compiled_circuit = transpile(qc, simulator)
    
    # Assemble the circuit
    qobj = assemble(compiled_circuit, shots=shots)
    
    # Run the simulation
    result = simulator.run(qobj).result()
    
    # Get measurement counts
    counts = result.get_counts()
    return counts

def write_counts_to_csv(counts, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Result', 'Count'])
        for key, value in counts.items():
            writer.writerow([key, value])

# Main execution
if __name__ == "__main__":
    # Generate the circuit
    qc = generate_60_qubit_circuit()

    # Run the simulation
    counts = run_simulation(qc)

    # Write results to CSV
    csv_filename = 'results.csv'
    write_counts_to_csv(counts, csv_filename)

