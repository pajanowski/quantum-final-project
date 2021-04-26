import pprint


def comparator(a, b):
    a = bool(int(a))
    b = bool(int(b))
    ret = a or not b
    return ret, ret ^ b

# compares two 4 bit values i.e. 1010 and 1001 would return 1
# compares as in ABCD >= EFGH
def two_four_bit_comparator(A, B, C, D, E, F, G, H):
    output = (A and not B and not C and not D and not E and not F and not G and H) or (
                A and not B and not C and not E and not F and G and not H) or (
                       A and not B and not C and D and not E and not F and G and H) or (
                       A and not B and not D and not E and not F and G and H) or (
                       A and not B and C and not D and not E and F and not G and H) or (
                       A and not B and not E and F and not G and not H) or (
                       A and not B and D and not E and F and not G and H) or (
                       A and not B and C and not E and F and G and not H) or (
                       A and not B and C and D and not E and F and G and H) or (
                       B and not C and not D and not E and not F and not G and H) or (
                       A and not C and not D and not E and F and not G and H) or (
                       A and B and not C and not D and E and not F and not G and H) or (
                       B and not C and not E and not F and G and not H) or (
                       B and not C and D and not E and not F and G and H) or (
                       A and not C and not E and F and G and not H) or (
                       A and not C and D and not E and F and G and H) or (
                       A and B and not C and E and not F and G and not H) or (
                       A and B and not C and D and E and not F and G and H) or (
                       C and not D and not E and not F and not G and H) or (
                       B and not D and not E and not F and G and H) or (
                       B and C and not D and not E and F and not G and H) or (
                       A and not D and not E and F and G and H) or (
                       A and C and not D and E and not F and not G and H) or (
                       A and B and not D and E and not F and G and H) or (
                       A and B and C and not D and E and F and not G and H) or (
                       not E and not F and not G and not H) or (D and not E and not F and not G and H) or (
                       C and not E and not F and G and not H) or (C and D and not E and not F and G and H) or (
                       B and not E and F and not G and not H) or (B and D and not E and F and not G and H) or (
                       B and C and not E and F and G and not H) or (B and C and D and not E and F and G and H) or (
                       A and E and not F and not G and not H) or (A and D and E and not F and not G and H) or (
                       A and C and E and not F and G and not H) or (A and C and D and E and not F and G and H) or (
                       A and B and E and F and not G and not H) or (A and B and D and E and F and not G and H) or (
                       A and B and C and E and F and G and not H) or (A and B and C and D and E and F and G and H)

    return output, B ^ output, C ^ output, D ^ output, E ^ output, F ^ output, G ^ output, H ^ output


def get_truth_table():
    bit_string_len = 4
    max_number = 2 ** bit_string_len
    ret = []
    for i in range(max_number):
        A = format(i, 'b').zfill(bit_string_len)
        for j in range(max_number):
            B = format(j, 'b').zfill(bit_string_len)
            row = []
            row.append(A)
            row.append(B)
            # for k in range(bit_string_len):
            #     result = comparator(A[k], B[k])
            #     row.append(int(result[0]))
            row.append(i >= j)
            ret.append(row)
    collapsed = []
    ret.sort()
    # ret = list(ret for ret, _ in itertools.groupby(ret))
    pprint.pprint(ret)


def run():
    A = '100'
    B = '011'

    ret = []

    for i in range(len(A)):
        ret.append(comparator(A[i], B[i]))
    print(ret)


if __name__ == '__main__':
    get_truth_table()
