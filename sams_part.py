import math from qiskit.circuit.library 
import IntegerComparator from qiskit 
import IBMQ, Aer, assemble, transpile 
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc

def num_comp(n1,n2,n3,n4,y1,y2,y3,y4,lst):

    qc = QuantumCircuit(4, 1)
    qc.reset(range(4))

    if n1==1:
        qc.x(3)
    if n2==1:
        qc.x(2)
    if n3==1:
        qc.x(1)
    if n4==1:
        qc.x(0)

    # barrier between input state and gate operation
    qc.barrier()



    n_bin_string = "0b" + str(n1) + str(n2) + str(n3) + str(n4)
    print('n bin string: ', n_bin_string)
    y_bin_string = "0b" + str(y1) + str(y2) + str(y3) + str(y4)
    print('y bin string: ', y_bin_string)

    if (lst[int(n_bin_string,2)] < lst[int(y_bin_string,2)]):
        qc.x(0)
        qc.x(1)
        qc.x(2)
        qc.x(3)
        qc.measure_all()

    else:
        qc.measure_all()
    # this is where your program for quantum XOR gate goes

    # barrier between input state and gate operation
    qc.barrier()

    #We'll run the program on a simulator
    backend = Aer.get_backend('qasm_simulator')
    #Since the output will be deterministic, we can use just a single shot to get it
    job = execute(qc, backend, shots=1, memory=True)
    output = job.result().get_memory()[0]

    return qc, output

def grover():
    number_of_qibits = math.ceil(math.log(n))
    L = get_L(16)
    y = random.choice(range(n))

    print(L)

    grover_circuit = initialize_s(grover_circuit, [0,1,2,3])

    #comparator = IntegerComparator(num_state_qubits=number_of_qibits, value=1, geq=True, name='cmp')

    qc_comp, out = num_comp(0,0,0,1,0,0,1,0,L)
    print(qc_comp)
    grover_circuit.append(qc_comp, range(n))

    grover_circuit.h([0,1,2,3])
    grover_circuit.z([0,1,2,3])
    grover_circuit.cz(0,3)
    grover_circuit.h([0,1,2,3])

    print('Comparing ',L[1],' < ',L[2],' gives output',out)

    print(grover_circuit)
    
grover()
