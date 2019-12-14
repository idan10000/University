# Skeleton file for HW3 - Fall 2019/20 - extended intro to CS

# Add your implementation to this file

# You may add other utility functions to this file,
# but you may NOT change the signature of the existing ones.

# Change the name of the file to include your ID number (hw3_ID.py).


import random
import math


############
# QUESTION 2
############

# a
def root(x, m, e=10 ** -8):
    left = 1
    right = x
    while left < right:
        mid = (left + right) / 2
        if abs(x - mid ** m) <= e:
            return mid
        if x - mid ** m > 0:
            left = mid
        else:
            right = mid
    return None


# b
def root2(x, m, e=10 ** -8):
    left = 1
    right = 1

    while right ** m < x:
        left = right
        right *= 2

    while left < right:
        mid = (left + right) / 2
        if abs(x - mid ** m) <= e:
            return mid
        if x - mid ** m > 0:
            left = mid
        else:
            right = mid
    return None


# c
def root3(x, m, e=10 ** -8):
    return NR(lambda y: y ** m - x, lambda y: m * (y ** (m - 1)), e)


def NR(func, deriv=None, epsilon=10 ** (-8), n=100, x0=None):
    if deriv is None:
        deriv = diff_param(func)
    if x0 is None:
        x0 = random.uniform(-100.0, 100.0)
    x = x0
    y = func(x)
    for i in range(n):
        if abs(y) < epsilon:
            print("x=", x, "f(x)=", y, "convergence in", i, "iterations")
            return x
        elif abs(deriv(x)) < 10 ** (-25):  # arbitrary small value
            print("zero derivative, x0=", x0, " i=", i, " xi=", x)
            return None
        else:
            print("x=", x, "f(x)=", y)
            x = x - func(x) / deriv(x)
            y = func(x)
    print("no convergence, x0=", x0, " i=", i, " xi=", x)
    return None


def diff_param(f, h=0.001):
    return (lambda x: (f(x + h) - f(x)) / h)


############
# QUESTION 3
############

# a
def swap(lst, i, j):
    tmp = lst[i]
    lst[i] = lst[j]
    lst[j] = tmp


def selection_sort(lst):
    """ sort lst (in-place) """
    n = len(lst)
    for i in range(n):
        m_index = i
        for j in range(i + 1, n):
            if lst[m_index] > lst[j]:
                m_index = j
        swap(lst, i, m_index)
    return None


def generate_sorted_blocks(lst, k):
    smallLists = list()
    for i in range(0, len(lst), k):
        temp = lst[i:i + k]
        selection_sort(temp)
        smallLists.append(temp)
    return smallLists


def merge(A, B):
    """ merging two lists into a sorted list
        A and B must be sorted! """
    n = len(A)
    m = len(B)
    C = [0 for i in range(n + m)]

    a = 0
    b = 0
    c = 0
    while a < n and b < m:  # more element in both A and B
        if A[a] < B[b]:
            C[c] = A[a]
            a += 1
        else:
            C[c] = B[b]
            b += 1
        c += 1

    C[c:] = A[a:] + B[b:]  # append remaining elements (one of those is empty)

    return C


def binaryMerge(lst):
    newList = list()
    if len(lst) % 2 == 1:
        newList.append(lst[len(lst) // 2])
    for i in range(len(lst) // 2):
        newList.append(merge(lst[i], lst[-i - 1]))
    return newList


# c
def merge_sorted_blocks(lst):
    sortedList = list()
    sortedList = binaryMerge(lst)
    m = len(sortedList)
    while m > 0:
        sortedList = binaryMerge(sortedList)
        m //= 2
    return sortedList[0]


def sort_by_block_merge(lst, k):
    return merge_sorted_blocks(generate_sorted_blocks(lst, k))


############
# QUESTION 4
############

def find_missing(lst, n):
    leftEdge = 0
    rightEdge = len(lst) - 1
    while leftEdge < rightEdge:
        mid = math.ceil((leftEdge + rightEdge) / 2)
        if mid == rightEdge:
            return rightEdge
        if lst[mid] != mid:
            rightEdge = mid
        else:
            leftEdge = mid
    return n


def binarySearch(lst, leftEdge, rightEdge, x):
    mid = math.ceil((leftEdge + rightEdge) / 2)
    while leftEdge <= rightEdge:
        if lst[mid] == x:
            return mid
        elif lst[mid] < x:
            leftEdge = mid
        else:
            rightEdge = mid - 1
        mid = math.ceil((leftEdge + rightEdge) / 2)

    return None


def find(lst, s):
    leftEdge = 0
    rightEdge = len(lst) - 1
    mid = math.ceil((leftEdge + rightEdge) / 2)
    while mid != rightEdge:
        if lst[mid] > lst[rightEdge]:
            leftEdge = mid
        else:
            rightEdge = mid
        mid = math.ceil((leftEdge + rightEdge) / 2)
    if lst[0] == s:
        return 0
    elif lst[0] < s:
        leftEdge = 0
        rightEdge -= 1
    else:
        leftEdge = rightEdge
        rightEdge = len(lst) - 1
    return binarySearch(lst, leftEdge, rightEdge, s)


def find2(lst, s):
    for i in range(len(lst)):
        if lst[i] == s:
            return i
    return None


############
# QUESTION 5
############

# a'
def string_to_int(s):
    sum = 0
    l = len(s)
    pos = 1
    for char in s:
        sum += (ord(char) - 97) * (5 ** (l - pos))
        pos += 1
    return sum


# b
def int_to_string(k, n):
    assert 0 <= n <= 5 ** k - 1
    str = ""
    for i in range(k):
        cur = n % 5
        str += chr(97 + cur)
        n //= 5
    return str[::-1]


# c
def sort_strings1(lst, k):
    supList = [0 for i in range(5 ** k)]
    for smallList in lst:
        supList[string_to_int(smallList)] += 1
    sortedList = []
    for i in range(5 ** k):
        for j in range(supList[i]):
            sortedList.append(int_to_string(k,i))
        if len(sortedList) == len(lst):
            return sortedList



# e
def sort_strings2(lst, k):
    sortedList = []
    for i in range(5 ** k):
        curString = int_to_string(k, i)
        repeats = lst.count(curString)
        for j in range(repeats):
            sortedList.append(curString)
        if len(sortedList) == len(lst):
            return sortedList



########
# Tester
########

def test():
    # q2
    epsilon = 1e-4

    x = 9
    m = 2
    res = root(x, m)
    if abs(x - pow(res, 2)) >= epsilon:
        print("error in root")

    res2 = root2(x, m)
    if abs(x - pow(res2, 2)) >= epsilon:
        print("error in root2")

    res3 = root3(x, m)
    if abs(x - pow(res3, 2)) >= epsilon:
        print("error in root3")

    # q3
    lst = [610, 906, 308, 759, 15, 389, 892, 939, 685, 565]
    if generate_sorted_blocks(lst, 2) != \
            [[610, 906], [308, 759], [15, 389], [892, 939], [565, 685]]:
        print("error in generate_sorted_blocks")
    if generate_sorted_blocks(lst, 3) != \
            [[308, 610, 906], [15, 389, 759], [685, 892, 939], [565]]:
        print("error in generate_sorted_blocks")
    if generate_sorted_blocks(lst, 10) != \
            [[15, 308, 389, 565, 610, 685, 759, 892, 906, 939]]:
        print("error in generate_sorted_blocks")

    block_lst1 = [[610, 906], [308, 759], [15, 389], [892, 939], [565, 685]]
    if merge_sorted_blocks(block_lst1) != \
            [15, 308, 389, 565, 610, 685, 759, 892, 906, 939]:
        print("error in merge_sorted_blocks")
    block_lst2 = [[308, 610, 906], [15, 389, 759], [685, 892, 939], [565]]
    if merge_sorted_blocks(block_lst2) != \
            [15, 308, 389, 565, 610, 685, 759, 892, 906, 939]:
        print("error in merge_sorted_blocks")

    # q4
    missing = find_missing([0,1,2,3,5], 5)
    if missing != 4:
        print("error in find_missing")

    pos = find([30, 40, 50, 60, 10, 20], 60)
    if pos != 3:
        print("error in find")

    pos = find([30, 40, 50, 60, 10, 20], 0)
    if pos != None:
        print("error in find")

    pos = find2([30, 40, 50, 60, 60, 20], 60)
    if pos != 3 and pos != 4:
        print("error in find2")

    # q5
    lst_num = [random.choice(range(5 ** 4)) for i in range(15)]
    for i in lst_num:
        s = int_to_string(4, i)
        if s is None or len(s) != 4:
            print("error in int_to_string")
        if (string_to_int(s) != i):
            print("error in int_to_string or in string_to_int")

    lst1 = ['aede', 'adae', 'dded', 'deea', 'cccc', 'aacc', 'edea', 'becb', 'daea', 'ccea']
    if sort_strings1(lst1, 4) \
            != ['aacc', 'adae', 'aede', 'becb', 'cccc', 'ccea', 'daea', 'dded', 'deea', 'edea']:
        print("error in sort_strings1")

    if sort_strings2(lst1, 4) \
            != ['aacc', 'adae', 'aede', 'becb', 'cccc', 'ccea', 'daea', 'dded', 'deea', 'edea']:
        print("error in sort_strings2")

print ((81)%7)

