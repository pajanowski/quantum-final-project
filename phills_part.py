import math
import random

from qiskit import *


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


# N number to convert to superposition
# returns super position in form of [[int]]
# i.e. N = 1 returns [[0],[1]]
# i.e. N = 2 returns [[0],[0],[1]]
def get_superposition(n, size):
    if size < 2:
        size = 2
    ret = []
    binary_string = format(n + 1, 'b').zfill(size)
    for i in range(len(binary_string) - 1, -1, -1):
        ret.append([int(binary_string[i])])
    return ret


def run():
    N = 4
    L = get_L(N)
    number_of_qibits = math.ceil(math.log(N))
    get_superposition()
    circuit = QuantumCircuit(number_of_qibits)



if __name__ == '__main__':
    run()

