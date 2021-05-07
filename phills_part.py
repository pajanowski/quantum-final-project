import ast
import math
import random
from typing import Tuple, Union, List

from numpy import pi
from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import LogicalExpressionOracle, CustomCircuitOracle, Oracle
from qiskit.circuit import classical_function, Int1
from qiskit.circuit.library import *
from qiskit.result import Counts
from qiskit.utils import QuantumInstance
from sympy.codegen import ast

from utils import *

from qiskit import *
from qiskit.extensions import Initialize
from qiskit.visualization import plot_histogram

L = []
y = 0
N = 0


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
    global L, y, N
    N = 16
    L = get_L(N)
    y = random.choice(range(N))
    m = 20
    for i in range(m):
        print(f"y = {y} | {format(y, 'b').zfill(4)}")
        print(f"L[y] = {L[y]}")
        number_of_qibits = math.ceil(math.log(N, 2))
        qreg = QuantumRegister(number_of_qibits)
        output = QuantumRegister(number_of_qibits)
        creg = ClassicalRegister(number_of_qibits)
        # qc = QuantumCircuit(register)
        # for i in range(number_of_qibits):
        #     qc.h(register[i])
        # # oracle.append(IntegerComparator(number_of_qibits, L[y]))
        # qc.z([0, 1, 2, 3])
        # qc.cz(0, 3)
        # qc.h([0, 1, 2, 3])

        result = grover_with_logical_expression()

        # result = grover_with_custom_circuit(number_of_qibits, output, qreg)
        # backend = BasicAer.get_backend('qasm_simulator')
        # results = execute(grover, backend, shots=1000).result()
        # counts = results.get_counts(grover)
        # print(result)
        measurements = result.get('measurement')
        # print(measurements)
        get_formatted_measurements(measurements)
        plot_histogram(measurements)

        # amplified_state = get_amplified_state(counts)
        y_primed = int("0b" + str(result.get('top_measurement')), 2)
        # print(f"amplified_state {amplified_state}")
        set_new_y(y_primed)

    print(f"final result of grover search, smallest y = {y} L[y] = {L[y]}")
    print(f"final result of y should be {L.index(0)}")


def get_formatted_measurements(measurements: dict):
    ret = {}
    for measurement in measurements.items():
        ret[str(int("0b" + str(measurement[0]), 2))] = measurement[1], measurement[0]
    print(ret)

def grover_with_custom_circuit(number_of_qibits, output, qreg):
    qc = QuantumCircuit(qreg, output, name='qc')
    for i in range(number_of_qibits):
        qc.h(qreg[i])
    circuit_oracle = CustomCircuitOracle(variable_register=qreg, output_register=qreg, circuit=qc,
                                         evaluate_classically_callback=f_L)
    grover = Grover(oracle=circuit_oracle)
    result = grover.run(QuantumInstance(BasicAer.get_backend('qasm_simulator'), shots=1024))
    return result


def grover_with_logical_expression():
    expression = get_boolean_functions_from_truth_table_logical_oracle()
    grover = Grover(oracle=LogicalExpressionOracle(expression=expression, optimization=True))
    return grover.run(QuantumInstance(BasicAer.get_backend('qasm_simulator'), shots=1024))


def set_new_y(y_primed):
    global L, y
    print(f"old y value {y}")
    if L[y_primed] < L[y]:
        y = y_primed
    print(f"new y value {y}")


def get_amplified_state(counts: Counts):
    highest = ('0', 0)
    for count in counts.items():
        if highest[1] < count[1]:
            highest = count
    return highest


def draw(qc: QuantumCircuit):
    qc.draw(output='mpl')


def get_boolean_functions_from_truth_table():
    global N
    variables = [' {0} ', ' {1} ', ' {2} ', ' {3} ']
    table = get_truth_table()
    # table = '0000000000000001'
    OR = ' or '
    AND = ' and '
    NOT = ' not '
    clauses = []
    truth_string = boolean_function_builder(AND, NOT, OR, clauses, table, variables)
    return truth_string


def boolean_function_builder(AND, NOT, OR, clauses, table, variables):
    global N
    for i in range(len(table)):
        if table[i] == '1':
            cur_clause = ' ( '
            B = format(i, 'b').zfill(int(math.log2(N)))
            for j in range(len(B)):
                if B[j] == '0':
                    cur_clause += NOT
                cur_clause += variables[j]
                if j < (len(B) - 1):
                    cur_clause += AND
            cur_clause += ' ) '
            clauses.append(cur_clause)
    # if there were no clauses generated that means the truth table returned all 0's
    # meaning that L[y] is already lowest so we just let all states through
    if len(clauses) == 0:
        clauses.append(OR.join(variables))
    truth_string = OR.join(clauses).replace('  ', ' ')
    return truth_string


def get_boolean_functions_from_truth_table_logical_oracle():
    variables = ['w', 'x', 'y', 'z']
    table = get_truth_table()
    OR = ' | '
    AND = ' & '
    NOT = ' ~'
    clauses = []
    truth_string = boolean_function_builder(AND, NOT, OR, clauses, table, variables)
    return truth_string


def f_L(bits: str) -> Tuple[bool, List[int]]:
    global L, y
    # just gonna assume that bits is 4 bytes long
    function = get_boolean_functions_from_truth_table()
    # replaced_function = function.replace('{3}', str(bool(int(bits[3]))))
    # replaced_function = replaced_function.replace('{2}', str(bool(int(bits[2]))))
    # replaced_function = replaced_function.replace('{1}', str(bool(int(bits[1]))))
    # replaced_function = replaced_function.replace('{0}', str(bool(int(bits[0]))))
    replaced_function = function
    for i in range(len(bits)):
        replaced_function = replaced_function.replace(f"{{{i}}}", str(bool(int(bits[i]))))
    ret = eval(replaced_function)
    try:
        assert ret == (int(bits, 2) < L[y])
    except Exception:
        print(f"Failed on {int(bits, 2)} < {L[y]}")
        print(f"bits looks like {bits}")
        print(f"Expression looks like {replaced_function}")
        function_parts = function.split('^')
        for function_part in function_parts:
            print(f"{function_part} evaluated to {eval(function_part)}")
        raise AssertionError
    ret_list = [ret]
    for bit in bits:
        ret_list.append(int(ret ^ bool(bit)))
    # ret_list = [8, 9, 4, 7]
    return ret, ret_list


def get_truth_table():
    global L, y
    truth_table = ''
    L_y = L[y]
    for i in range(len(L)):
        if L[i] < L_y:
            truth_table += '0'
            print(f"L[{i}] is less than L[y]")
            print(f"L[{i}] = {L[i]}")
        else:
            truth_table += '1'
    print(f"truth table = {truth_table}")
    return truth_table


if __name__ == '__main__':
    run()
