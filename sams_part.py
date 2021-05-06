import math from qiskit.circuit.library 
import IntegerComparator from qiskit 
import IBMQ, Aer, assemble, transpile 
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def initialize_s(qc, qubits):
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
    
def num_comp(inp1,inp2,inp3,inp4, l_y):

    qc = QuantumCircuit(4, 1)
    qc.reset(range(4))

    if inp1==1:
        qc.x(0)
    if inp2==1:
        qc.x(1)
    if inp3==1:
        qc.x(2)
    if inp4==1:
        qc.x(3)

    # barrier between input state and gate operation
    qc.barrier()

    if inp1==1:
        qc.x(0)
    if inp2==1:
        qc.x(1)
    if inp3==1:
        qc.x(2)

    bin_string = "0b" + str(inp1) + str(inp2) + str(inp3) + str(inp4)
    if (int(bin_string,2) < l_y and inp4 == 0):
        qc.x(3)
        qc.measure(3,0)
    if (int(bin_string,2) > l_y and inp4 == 1):
        qc.x(3)
        qc.measure(3,0)
    qc.x(3)
    # this is where your program for quantum XOR gate goes

    # barrier between input state and gate operation
    qc.barrier()

    #Remove comment below to check if the output has been reversed to match input
    #qc.measure(3,0)


    #We'll run the program on a simulator
    backend = Aer.get_backend('qasm_simulator')
    #Since the output will be deterministic, we can use just a single shot to get it
    job = execute(qc, backend, shots=1, memory=True)
    output = job.result().get_memory()[0]

    return qc, output
