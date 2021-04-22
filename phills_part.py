import math
import random
from utils import *

from qiskit import *
from qiskit.extensions import Initialize
from qiskit.visualization import plot_histogram

def get_pi_perm(n):
    pi = {}
    set = []
    for i in range(n):
        set.append(i)

    set_len = int(len(set) / 2)
    for i in range(set_len):
        key = random.choice(set)
        set.remove(key)
        value = random.choice(set)
        set.remove(value)
        pi[key] = value
        pi[value] = key
    return pi

# N integer
def get_L(N):
    ret = []
    pi_perm = get_pi_perm(N)
    for i in range(len(pi_perm.keys())):
        ret.append(pi_perm.get(i))
    return ret


def run():
    N = 4
    L = get_L(N)
    y = random.choice(range(N))
    number_of_qibits = math.ceil(math.log(N))
    register = QuantumRegister(number_of_qibits)
    qc = QuantumCircuit(register)
    # initializer = Initialize(scalar(1 / math.sqrt(N), get_superposition(n, number_of_qibits)))
    # qc.append(initializer, )
    for i in range(number_of_qibits):
        qc.h(register[i])

    qc.measure_all()

    backend = BasicAer.get_backend('qasm_simulator')
    results = execute(qc, backend, shots=1000).result()
    counts = results.get_counts(qc)
    print(counts)
    plot_histogram(counts)

if __name__ == '__main__':
    run()

