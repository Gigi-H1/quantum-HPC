from qiskit_aer import Aer

# Initialize a GPU backend
# Note that the cloud instance for tutorials does not have a GPU
# so this will raise an exception.
try:
    simulator_gpu = Aer.get_backend(method="statevector", "device":"GPU")

except Aer as e:
    print(e)

