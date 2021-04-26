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
    qr = QuantumRegister(number_of_qibits, 'q1')
    cr = ClassicalRegister(number_of_qibits, 'c1')
    qc = QuantumCircuit(qr, cr)
    # initializer = Initialize(scalar(1 / math.sqrt(N), get_superposition(n, number_of_qibits)))
    # qc.append(initializer, )
    for i in range(number_of_qibits):
        qc.h(qr[i])

    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.draw(output='mpl')
    # qc.ms()
    L_y = L[y]
    # L_n = L[cr]
    #
    # if L_n < L_y:
    #     cr[0] = -1 * cr[0]
    #
    #
    #
    #
    backend = BasicAer.get_backend('qasm_simulator')
    results = execute(qc, backend, shots=1000).result()
    counts = results.get_counts(qc)
    print(counts)
    plot_histogram(counts)


if __name__ == '__main__':
    run()

