import math
import random
from typing import Tuple

from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import LogicalExpressionOracle
from qiskit.circuit import classical_function, Int1
from qiskit.circuit.library import IntegerComparator

from utils import *

from qiskit import *
from qiskit.extensions import Initialize
from qiskit.visualization import plot_histogram

L = []
y = 0
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
    global L, y
    N = 16
    L = get_L(N)
    y = random.choice(range(N))
    number_of_qibits = math.ceil(math.log(N, 2))
    register = QuantumRegister(number_of_qibits)
    qc = QuantumCircuit(register)
    for i in range(number_of_qibits):
        qc.h(register[i])

    qc.measure_all()

    oracle = QuantumCircuit(number_of_qibits, 1)

    # oracle.append(IntegerComparator(number_of_qibits, L[y]))
    oracle_circuit = oracle_comparator.synth()
    oracle.append(oracle_circuit)
    oracle.draw(output='mpl')

    grover_operator = Grover(oracle=oracle).grover_operator
    qc.append(grover_operator)

    backend = BasicAer.get_backend('qasm_simulator')
    results = execute(qc, backend, shots=1000).result()
    counts = results.get_counts(qc)
    print(counts)
    plot_histogram(counts)


@classical_function
def oracle_comparator(ln0: Int1, ln1: Int1, ln2: Int1, ln3: Int1, ly0: Int1, ly1: Int1, ly2: Int1, ly3: Int1) -> Int1:
    output = (ln0 and not ln1 and not ln2 and not ln3 and not ly0 and not ly1 and not ly2 and ly3) or (
            ln0 and not ln1 and not ln2 and not ly0 and not ly1 and ly2 and not ly3) or (
                     ln0 and not ln1 and not ln2 and ln3 and not ly0 and not ly1 and ly2 and ly3) or (
                     ln0 and not ln1 and not ln3 and not ly0 and not ly1 and ly2 and ly3) or (
                     ln0 and not ln1 and ln2 and not ln3 and not ly0 and ly1 and not ly2 and ly3) or (
                     ln0 and not ln1 and not ly0 and ly1 and not ly2 and not ly3) or (
                     ln0 and not ln1 and ln3 and not ly0 and ly1 and not ly2 and ly3) or (
                     ln0 and not ln1 and ln2 and not ly0 and ly1 and ly2 and not ly3) or (
                     ln0 and not ln1 and ln2 and ln3 and not ly0 and ly1 and ly2 and ly3) or (
                     ln1 and not ln2 and not ln3 and not ly0 and not ly1 and not ly2 and ly3) or (
                     ln0 and not ln2 and not ln3 and not ly0 and ly1 and not ly2 and ly3) or (
                     ln0 and ln1 and not ln2 and not ln3 and ly0 and not ly1 and not ly2 and ly3) or (
                     ln1 and not ln2 and not ly0 and not ly1 and ly2 and not ly3) or (
                     ln1 and not ln2 and ln3 and not ly0 and not ly1 and ly2 and ly3) or (
                     ln0 and not ln2 and not ly0 and ly1 and ly2 and not ly3) or (
                     ln0 and not ln2 and ln3 and not ly0 and ly1 and ly2 and ly3) or (
                     ln0 and ln1 and not ln2 and ly0 and not ly1 and ly2 and not ly3) or (
                     ln0 and ln1 and not ln2 and ln3 and ly0 and not ly1 and ly2 and ly3) or (
                     ln2 and not ln3 and not ly0 and not ly1 and not ly2 and ly3) or (
                     ln1 and not ln3 and not ly0 and not ly1 and ly2 and ly3) or (
                     ln1 and ln2 and not ln3 and not ly0 and ly1 and not ly2 and ly3) or (
                     ln0 and not ln3 and not ly0 and ly1 and ly2 and ly3) or (
                     ln0 and ln2 and not ln3 and ly0 and not ly1 and not ly2 and ly3) or (
                     ln0 and ln1 and not ln3 and ly0 and not ly1 and ly2 and ly3) or (
                     ln0 and ln1 and ln2 and not ln3 and ly0 and ly1 and not ly2 and ly3) or (
                     not ly0 and not ly1 and not ly2 and not ly3) or (ln3 and not ly0 and not ly1 and not ly2 and ly3) or (
                     ln2 and not ly0 and not ly1 and ly2 and not ly3) or (ln2 and ln3 and not ly0 and not ly1 and ly2 and ly3) or (
                     ln1 and not ly0 and ly1 and not ly2 and not ly3) or (ln1 and ln3 and not ly0 and ly1 and not ly2 and ly3) or (
                     ln1 and ln2 and not ly0 and ly1 and ly2 and not ly3) or (ln1 and ln2 and ln3 and not ly0 and ly1 and ly2 and ly3) or (
                     ln0 and ly0 and not ly1 and not ly2 and not ly3) or (ln0 and ln3 and ly0 and not ly1 and not ly2 and ly3) or (
                     ln0 and ln2 and ly0 and not ly1 and ly2 and not ly3) or (ln0 and ln2 and ln3 and ly0 and not ly1 and ly2 and ly3) or (
                     ln0 and ln1 and ly0 and ly1 and not ly2 and not ly3) or (ln0 and ln1 and ln3 and ly0 and ly1 and not ly2 and ly3) or (
                     ln0 and ln1 and ln2 and ly0 and ly1 and ly2 and not ly3) or (ln0 and ln1 and ln2 and ln3 and ly0 and ly1 and ly2 and ly3)

    return output

if __name__ == '__main__':
    run()

