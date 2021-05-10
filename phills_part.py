import ast
import math
import random
from typing import Tuple, Union, List

from matplotlib.figure import Figure
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
    # L = [3, 5, 8, 0, 6, 1, 4, 13, 2, 15, 12, 14, 10, 7, 11, 9]
    print(f"L = {L}")
    print(f"index containing 0 = {L.index(0)}")
    # y = random.choice(range(N))
    y = L.index(15)
    # y = 9
    m = 5
    for i in range(m):
        print(f"y = {y} | {get_int_as_bit_string(y)}")
        print(f"L[y] = {L[y]}")
        number_of_qibits = math.ceil(math.log(N, 2))

        """
        This is the function for the mostly working grover search using an oracle that isn't reversible.
        """
        result = grover_with_logical_expression()

        """
        This is the function for the non working grover search using an oracle that is reversible.
        """
        # result = grover_with_custom_circuit(number_of_qibits)

        measurements = result.get('measurement')

        top_measurement_item = ('0000', 0)
        for measurement in measurements.items():
            if measurement[1] > top_measurement_item[1]:
                top_measurement_item = measurement

        print(f"all measurements {get_formatted_measurements(measurements)}")
        print(f"marked measurements {get_formatted_measurements(measurements, show_correct_marked_values_only=True)}")
        print(f"marked reversed measurements {get_formatted_measurements(measurements, reverse_bits=True, show_correct_marked_values_only=True)}")

        # amplified_state = get_amplified_state(counts)
        top_measurement = top_measurement_item[0]
        print(f"top_measurement = {top_measurement}")
        print(f"rev_top_measurement = {top_measurement[::-1]}")

        print(f"L[y_top] = {L[get_int_from_bit_string(top_measurement)]}, L[y_top_rev] = {L[get_int_from_bit_string(top_measurement[::-1])]}")

        histogram: Figure = plot_histogram(measurements)
        top_measurement_int = get_int_from_bit_string(top_measurement)
        histogram.suptitle(f"L[y] = {L[y]} Top Measurement n = {str(top_measurement_int)} L[n] = {str(L[top_measurement_int])}")
        histogram.savefig(f"{i}.png")

        """
        For some g darn reason the top_measurement, the bit string that grover spits out, is the correct order on 
        the first go iteration but not for any of the following. That's the why this caveat is here that basically 
        defeats the point of putting it through a quantum circuit, so its staying commented out. I have tried reversing 
        the truth table, the logical expression, and the top_measurement en masse to no avail. I noticed this after 
        seeing the circuit succeed when the L[0] index was a number that when converted to a bit string was reversible. 
        i.e. 15 (1111), 6 (0110), 9 (1001).
        """
        # if i != 0:
        #     top_measurement = top_measurement[::-1]

        y_primed = int("0b" + str(top_measurement), 2)
        # print(f"amplified_state {amplified_state}")
        set_new_y(y_primed)
        print(f"finished run {i + 1} / {m}")

    print(f"final result of grover search, smallest y = {y} L[y] = {L[y]}")
    print(f"final result of y should be {L.index(0)}")


def get_int_as_bit_string(y):
    return format(y, 'b').zfill(4)


def get_formatted_measurements(measurements: dict, reverse_bits=False, show_correct_marked_values_only=False):
    """
    This is a logging function I was using to look at the measurements with the measured value, the number of hits, and
    the integer value of the measured values.

    :param measurements: the measurements being used
    :param reverse_bits: reverse the bits on the measurements and see if the values make sense then, usually they do
    :param show_correct_marked_values_only: only output the values that were expected to be marked.
                                            Using with reverse_bits helps a lot.
    :return: the constructed measurements
    """
    global L, y
    ret = {}
    for measurement in measurements.items():
        if reverse_bits:
            reversed_measurement = str(measurement[0][::-1])
            i = int("0b" + reversed_measurement, 2)
            if show_correct_marked_values_only:
                if L[i] < L[y]:
                    ret[str(i)] = measurement[1], reversed_measurement, L[i]
            else:
                ret[str(i)] = measurement[1], reversed_measurement, L[i]
        else:
            i = int("0b" + str(measurement[0]), 2)
            if show_correct_marked_values_only:
                if L[i] < L[y]:
                    ret[str(int("0b" + str(measurement[0]), 2))] = measurement[1], measurement[0], L[i]
            else:
                ret[str(int("0b" + str(measurement[0]), 2))] = measurement[1], measurement[0], L[i]
    return ret


def grover_with_custom_circuit(number_of_qibits):
    """
    This function is used to run the minimum search with grover's algorithm. It does everything but work. It creates a
    reversible boolean oracle function using the same function that the grover_with_logical_expression but for some
    reason the CustomCircuitOracle never marks anything. Sometimes it will get luck and the top measure will be the
    smallest valued index but don't let that fool you.
    :param number_of_qibits: log_2(n) of the number of indexes in N
    :return: the results of the search
    """
    qreg = QuantumRegister(number_of_qibits)
    output = QuantumRegister(number_of_qibits)
    # qc = QuantumCircuit(qreg, output)
    # qc.z([0, 1, 2, 3])
    # qc.cz(0, 3)
    # qc.h([0, 1, 2, 3])
    # for i in range(number_of_qibits):
    #     qc.h(qreg[i])
    qc = QuantumCircuit(qreg, output, name='oracle')
    circuit_oracle = CustomCircuitOracle(variable_register=qreg, output_register=output, circuit=qc,
                                         evaluate_classically_callback=f_L)
    grover = Grover(oracle=circuit_oracle)
    draw: Figure = grover.grover_operator.draw(output='mpl')
    draw.savefig('custom_circuit_grover.png')
    result = grover.run(QuantumInstance(BasicAer.get_backend('qasm_simulator'), shots=2048))
    return result


def grover_with_logical_expression():
    """
    This function is used to run the minimum search with grover's algorithm with the logical expression oracle.
    This one does work sometimes.

    I noticed at one point that the inverse of the correct bits were getting marked
    i.e. if index 3(0011) was supposed to be marked, then 12(1100) was getting marked.
    I never figured out what was going on here which is the such as for 0011 to be marked as opposed to 1100.
    I dug down deep into qiskit oracle source code and found nothing that would suggest the order of the bits are
    expected to be flipped. Probably something small that I've look at 100 times and thought that it was correct.

    :param number_of_qibits: log_2(n) of the number of indexes in N
    :return: the results of the search
    """
    expression = get_boolean_functions_from_truth_table_logical_oracle()
    oracle = LogicalExpressionOracle(expression=expression, optimization=True, mct_mode='noancilla')
    grover = Grover(oracle=oracle)
    draw: Figure = grover.grover_operator.draw(output='mpl')
    draw.savefig('logical_expression_grover.png')
    return grover.run(QuantumInstance(BasicAer.get_backend('qasm_simulator'), shots=2048))


def set_new_y(y_primed):
    """
    sets y = y_primed if L[y_primed] < L[y]
    :param y_primed:
    :return:
    """
    global L, y
    print(f"old y value {y} L[y] = {L[y]}")
    print(f"y_primed value {y_primed} L[y] = {L[y_primed]}")
    if L[y_primed] < L[y]:
        y = y_primed
    print(f"new y value {y} L[y] = {L[y]}")


def draw(qc: QuantumCircuit):
    """
    Function I used for debugging to save on typing
    :param qc: Quantum circuit you want drawn
    :return:
    """
    qc.draw(output='mpl')


def get_boolean_functions_from_truth_table():
    global N
    variables = [' {0} ', ' {1} ', ' {2} ', ' {3} ']
    table = get_truth_table()
    OR = ' or '
    AND = ' and '
    NOT = ' not '
    truth_string = boolean_function_builder(AND, NOT, OR, table, variables)
    return truth_string


def qc_from_logical_expression():
    logical_expression = get_boolean_functions_from_truth_table_logical_oracle()
    qc = qc_from_boolean_functions(logical_expression, '&', '~', '|')
    return qc


def qc_from_boolean_functions(boolean_functions: str, AND_op, NOT_op, OR_op):
    """
    pipe dream function to convert the boolean function to a quantum circuit to use as the oracle that never panned out
    I couldn't even get the multi control x gate to append correctly to the circuit.
    :param boolean_functions:
    :param AND_op:
    :param NOT_op:
    :param OR_op:
    :return:
    """
    boolean_functions_list = boolean_functions.split('|')
    qc = QuantumCircuit(5)
    for boolean_function in boolean_functions_list:
        boolean_function = boolean_function.strip('(')
        boolean_function = boolean_function.strip(')')
        params = boolean_function.split(AND_op)
        for i in range(len(params)):
            if NOT_op in params[i]:
                qc.x(i)

        qc.mcx(list(range(len(params))), 5, ancilla_qubits=1)

    return qc


def boolean_function_builder(AND, NOT, OR, table, variables):
    """
    I also added output to the boolean_function_builder method
    and the functions it is returning is are for the correct bit values
    :param AND: your AND symbol, 'and' or '&' most likely
    :param NOT: your NOT symbol, 'not' or '~'
    :param OR: 'or' or '|'
    :param table: the truth table string that this will be based on 10110101
    :param variables: Variable list that will be replaced with the bits when used.
    :return:
    """
    global N, y

    clauses = []
    print("\nBoolean Functions for Oracle")
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
            print(f"{cur_clause} clause for marking y={i} L[y]={L[i]}")
            clauses.append(cur_clause)
    # if there were no clauses generated that means the truth table returned all 0's
    # meaning that L[y] is already lowest so we just let all states through
    if len(clauses) == 0:
        clauses.append(OR.join(variables))
    truth_string = OR.join(clauses).replace('  ', ' ')
    return truth_string


def get_boolean_functions_from_truth_table_logical_oracle():
    """
    Creates the logical expression to be used as the expression in the logical expression oracle
    :return: logical expression that should mark the correct states based on the truth table
    """
    variables = ['a', 'b', 'c', 'd']
    table = get_truth_table()
    OR = ' | '
    AND = ' & '
    NOT = ' ~'
    truth_string = boolean_function_builder(AND, NOT, OR, table, variables)
    return truth_string


def f_L(bits: str) -> Tuple[bool, List[int]]:
    """
    This is the function that is used in the CustomCircuitOracle as the evaluate_classically_callback.
    This functions as intended I swear and returns the proper boolean value but the CustomCircuitOracle doesn't care.

    :param bits: bits that are passed in from the quantum circuit
    :return: boolean value and list of integers that will be the output of the oracle. In this case bit 0 is the output
             of the boolean function and the list of integers are the corresponding input bit xor'd with the output.
             i.e. [ret, [ret, ret ^ bit[1], ret ^ bit[2], ret ^ bit[3]]]
    """
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
    # try:
    #     assert ret == (int(bits, 2) < L[y])
    # except Exception:
    #     print(f"Failed on {int(bits, 2)} < {L[y]}")
    #     print(f"bits looks like {bits}")
    #     print(f"Expression looks like {replaced_function}")
    function_parts = replaced_function.split('^')
    if ret:
        print(f"inputs bits for f_L = {bits}")
        for function_part in function_parts:
            print(f"{replaced_function} evaluated to True")
    #     raise AssertionError
    ret_list = [ret]
    for bit in bits:
        ret_list.append(int(ret ^ bool(bit)))
    # ret_list = [8, 9, 4, 7]
    return ret, ret_list


def get_truth_table():
    """
    returns a bit string that corresponds to the truthiness of L[i] < L[y] where i is the place in the truth table string
    if L[y] = 15, i = 0 L[i] = 2, L[i] < L[y] is true and a 1 will be put in the 0th spot of the truth table
    :return: truth table string
    """
    global L, y
    truth_table = []
    L_y = L[y]
    for i in range(len(L)):
        # bit_string = get_int_as_bit_string(i)
        # i_rev = get_int_from_bit_string(bit_string[::-1])
        if L[i] < L_y:
            truth_table.append('1')
            # print(f"L[{i}] is less than L[y]")
            # print(f"L[{i}] = {L[i]}")
        else:
            truth_table.append('0')
    print(f"truth table = {truth_table}")
    return truth_table


def get_int_from_bit_string(bit_string):
    return int("0b" + bit_string, 2)


if __name__ == '__main__':
    run()
