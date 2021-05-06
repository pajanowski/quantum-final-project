import math
import random
from typing import Tuple

from numpy import pi
from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import LogicalExpressionOracle
from qiskit.circuit import classical_function, Int1
from qiskit.circuit.library import IntegerComparator, GroverOperator
from qiskit.result import Counts

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
    m = 10
    for i in range(m):
        number_of_qibits = math.ceil(math.log(N, 2))
        register = QuantumRegister(number_of_qibits)
        # qc = QuantumCircuit(register)
        # for i in range(number_of_qibits):
        #     qc.h(register[i])
        # # oracle.append(IntegerComparator(number_of_qibits, L[y]))
        # qc.z([0, 1, 2, 3])
        # qc.cz(0, 3)
        # qc.h([0, 1, 2, 3])

        oracle = QuantumCircuit(number_of_qibits)
        for i in range(number_of_qibits):
            oracle.h(i)

        # TODO append actual oracle part of the oracle here
        oracle.x(0)
        oracle.x(1)

        oracle.cp(pi / 4, 0, 3)
        oracle.cx(0, 1)
        oracle.cp(-pi / 4, 1, 3)
        oracle.cx(0, 1)
        oracle.cp(pi / 4, 1, 3)
        oracle.cx(1, 2)
        oracle.cp(-pi / 4, 2, 3)
        oracle.cx(0, 2)
        oracle.cp(pi / 4, 2, 3)

        oracle.x(0)
        oracle.x(1)
        oracle.cz(0, 1)

        grover_operator = GroverOperator(oracle=oracle)
        grover_operator.measure_all()
        backend = BasicAer.get_backend('qasm_simulator')
        results = execute(grover_operator, backend, shots=1000).result()
        counts = results.get_counts(grover_operator)
        print(counts)
        plot_histogram(counts)
        amplified_state = get_amplified_state(counts)
        y_primed = int("0b" + amplified_state[0], 2)
        print(f"amplified_state {amplified_state}")
        set_new_y(y_primed)


def set_new_y(y_primed):
    global L, y
    if L[y_primed] < L[y]:
        y = y_primed


def get_amplified_state(counts: Counts):
    highest = ('0', 0)
    for count in counts.items():
        if highest[1] < count[1]:
            highest = count
    return highest


def get_good_states(str):
    return ['1111']


def draw(qc: QuantumCircuit):
    qc.draw(output='mpl')

def get_truth_table():
    global L, y
    truth_table = ''
    L_y = L[y]
    for i in range(len(L)):
        if L[i] < L_y:
            truth_table += '1'
        else:
            truth_table += '0'
    return truth_table


if __name__ == '__main__':
    run()
