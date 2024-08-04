from qiskit_aer import AerError
from qiskit_aer import AerSimulator
# Initialize a GPU backend

try:
    simulator_gpu = AerSimulator.from_backend('aer_simulator')
    simulator_gpu.set_options(device='GPU')
except AerError as e:
    print(e)
