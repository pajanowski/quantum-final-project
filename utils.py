import copy


def scalar(multiplicand, matrix):
    ret = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            ret[i][j] = multiplicand * matrix[i][j]
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
