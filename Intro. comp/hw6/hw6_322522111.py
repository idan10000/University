# Skeleton file for HW6 - Winter 2019/20 - extended intro to CS

# Add your implementation to this file

# You may add other utility functions to this file,
# but you may NOT change the signature of the existing ones.

# Change the name of the file to include your ID number (hw6_ID.py).


############
# QUESTION 1
############

###### CODE FROM LECTURE - DO NOT CHANGE ######
def fingerprint(text, basis=2 ** 16, r=2 ** 32 - 3):
    """ used to compute karp-rabin fingerprint of the pattern
        employs Horner method (modulo r) """
    partial_sum = 0
    for ch in text:
        partial_sum = (partial_sum * basis + ord(ch)) % r
    return partial_sum


def text_fingerprint(text, m, basis=2 ** 16, r=2 ** 32 - 3):
    """ computes karp-rabin fingerprint of the text """
    f = []
    b_power = pow(basis, m - 1, r)
    list.append(f, fingerprint(text[0:m], basis, r))
    # f[0] equals first text fingerprint
    for s in range(1, len(text) - m + 1):
        new_fingerprint = ((f[s - 1] - ord(text[s - 1]) * b_power) * basis + ord(text[s + m - 1])) % r
        # compute f[s], based on f[s-1]
        list.append(f, new_fingerprint)  # append f[s] to existing f
    return f


##############################################


def is_rotated_1(s, t, basis=2 ** 16, r=2 ** 32 - 3):
    sFingerprint = fingerprint(s)
    tFingerprint = fingerprint(t)
    power = pow(basis, len(s) - 1, r)
    for i in range(len(s)):
        sFingerprint = ((sFingerprint - ord(s[i]) * power) * basis + ord(s[i])) % r
        if sFingerprint == tFingerprint:
            return True
    return False


def is_rotated_2(s, t):
    return fingerprint(s) in text_fingerprint(t * 2, len(s))


############
# QUESTION 2
############

def is_equal(a, b):
    return abs(a - b) < 0.0000000001


def is_leq(a, b):
    return a < b + 0.0000000001


def arithmetic_encode_env(st, p):
    a, b = 0, 1

    if st == "":
        return a, b
    return arithmetic_encode(a, b, 0, st, p)


def arithmetic_encode(a, b, pos, st, p):  # """FILL SIGNATURE WITH YOUR CODE"""):
    if pos == len(st) - 1:
        if st[-1] == "0":
            return a, a + (b - a) * p
        else:
            return a + (b - a) * p, b
    if st[pos] == "0":
        return arithmetic_encode(a, a + (b - a) * p, pos + 1, st, p)
    return arithmetic_encode(a + (b - a) * p, b, pos + 1, st, p)


def arithmetic_decode_env(a, b, p):
    return arithmetic_decode(a, b, p, 0, 1)


def arithmetic_decode(a, b, p, curA, curB):
    if is_equal(a, curA) and is_equal(b, curB):
        return ""
    if is_leq(b, curA + (curB - curA) * p):
        return "0" + arithmetic_decode(a, b, p, curA, curA + (curB - curA) * p)
    return "1" + arithmetic_decode(a, b, p, curA + (curB - curA) * p, curB)


from linked_list import Linked_list


############
# QUESTION 3
############
def maxmatch(T, p, triple_dict, w=2 ** 12 - 1, max_length=2 ** 5 - 1):
    """ finds a maximum match of length k<=2**5-1 in a w long window, T[p:p+k] with T[p-m:p-m+k].
        Returns m (offset) and k (match length) """

    assert isinstance(T, str)
    n = len(T)
    maxmatch = 0
    offset = 0
    if p + 3 > len(T) or T[p:p + 3] not in triple_dict:
        return offset, maxmatch
    ### START: fill-in your code here according to the instructions
    vals = triple_dict[T[p:p + 3]]
    for i in range(len(vals) - 1, -1, -1):
        if p - vals[i] <= w:
            k = 3
            while k < min(n - p, max_length) and T[vals[i] + k] == T[p + k]:
                k += 1
            if k > maxmatch:
                maxmatch = k
                offset = p - vals[i]
        else:
            break
    ### END
    return offset, maxmatch


def LZW_compress(text, w=2 ** 12 - 1, max_length=2 ** 5 - 1):
    """LZW compression of an ascii text. Produces a list comprising of either ascii characters
       or pairs [m,k] where m is an offset and k>=3 is a match (both are non negative integers) """
    result = []
    n = len(text)
    p = 0
    triple_dict = {}

    while p < n:
        m, k = maxmatch(text, p, triple_dict, w, max_length)
        ### START: fill-in your code here according to the instructions
        add_triple_to_dict(text, p, triple_dict)
        if k < 3:
            result.append(text[p])
            p += 1
        else:
            result.append([m, k])
            p += k
        ### END
    return result  # produces a list composed of chars and pairs


def add_triple_to_dict(text, p, triple_dict):
    """ Adds to the dictionary mapping from a key T[p:p+2] to a new
        integer in a list p."""
    if p + 3 > len(text): return
    triple = text[p:p + 3]
    if triple in triple_dict:
        triple_dict[triple].append(p)
    else:
        triple_dict[triple] = [p]


############
# QUESTION 5
############


def what2(l):
    node = l.next
    while node is not None:
        yield node
        node = node.next


############
# QUESTION 6
############

from matrix import Matrix


# (1)
def right_left(im):
    n, m = im.dim()
    im2 = Matrix(n, m)
    for i in range(n):
        for j in range(m):
            im2[i, j] = im[n - i, m - j]
    return im2


# (2)
def what(im):
    n, m = im.dim()
    im2 = Matrix(n, m)
    for i in range(n):
        # replace the following line with your answer:
        im2.rows[i] = sorted(im.rows[i])
    return im2


########
# Tester
########

def test():
    # Question 1
    for func in [is_rotated_1, is_rotated_2]:
        if func("amirrub", "rubamir") != True or \
                func("amirrub", "bennych") != False or \
                func("amirrub", "ubamirr") != True:
            print("error in", func.__name__)

    # Question 2
    if arithmetic_encode_env("0", 0.5) != (0.0, 0.5):
        print("error in arithmetic_encode_env")
    if arithmetic_encode_env("00", 0.5) != (0.0, 0.25):
        print("error in arithmetic_encode_env")
    if arithmetic_encode_env("01", 0.5) != (0.25, 0.5):
        print("error in arithmetic_encode_env")

    if arithmetic_decode_env(0.0, 0.5, 0.5) != "0":
        print("error in arithmetic_decode_env")
    if arithmetic_decode_env(0.0, 0.25, 0.5) != "00":
        print("error in arithmetic_decode_env")
    if arithmetic_decode_env(0.25, 0.5, 0.5) != "01":
        print("error in arithmetic_decode_env")

    # Question 3

    # first convert to tuple to make easy comparison
    compressed = tuple([el if isinstance(el, str) else tuple(el) for el in LZW_compress("abcdabc")])
    if compressed != ('a', 'b', 'c', 'd', (4, 3)):
        print("error in LZW_compress")
