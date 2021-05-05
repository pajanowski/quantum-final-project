import math from qiskit.circuit.library 
import IntegerComparator from qiskit 
import IBMQ, Aer, assemble, transpile 
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc
def grover():
    number_of_qibits = math.ceil(math.log(n))
    L = get_L(n)
    y = random.choice(range(n))
    grover_circuit = initialize_s(grover_circuit, [0,1,2,3])
    comparator = IntegerComparator(num_state_qubits=number_of_qibits, value=L[y], geq=True, name='cmp')
    grover_circuit.append(comparator, range(n))
    grover_circuit.h([0,1,2,3])
    grover_circuit.z([0,1,2,3])
    grover_circuit.cz(0,3)
    grover_circuit.h([0,1,2,3])
    print(grover_circuit)
