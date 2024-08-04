import numpy as np
import pandas as pd
from cuquantum import custatevec as cusv

# Set number of qubits
n_qubits = 3

# Initialize state vector in |000>
state_vector = np.zeros(2**n_qubits, dtype=np.complex128)
state_vector[0] = 1.0

# Create cuStateVec handle
handle = cusv.create()

# Apply an X gate to the first qubit (qubit 0)
cusv.apply_matrix(
    handle,
    state_vector,
    n_qubits,
    cusv.matrix_type.X,
    [0],  # Target qubit
    np.complex128
)

# Apply a Hadamard gate to the second qubit (qubit 1)
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
cusv.apply_matrix(
    handle,
    state_vector,
    n_qubits,
    H,
    [1],  # Target qubit
    np.complex128
)

# Save resulting state vector to a CSV file
result_df = pd.DataFrame(state_vector, columns=["StateVector"])
result_df.to_csv("quantum_simulation_results.csv", index=False)

# Clean up
cusv.destroy(handle)

