import time
import sys

############
# QUESTION 2
############
def onlyOneRemain(stacks):
    flag = False
    for stack in stacks:
        if stack is not 0:
            if flag:
                return False
            flag = True
    return True


def can_win_nim(stacks):
    if onlyOneRemain(stacks):
        return True
    for i in range(len(stacks)):
        for num in range(1, stacks[i] + 1):
            stacks[i] -= num
            flag = can_win_nim(stacks)
            stacks[i] += num
            if not flag:
                return True
    return False


def can_win_nim_mem(stacks):
    d = {}
    return canWinNimMemRec(stacks, d)

def canWinNimMemRec(stacks, dictionary):
    if onlyOneRemain(stacks):
        return True
    for i in range(len(stacks)):
        for num in range(1, stacks[i] + 1):
            tupStacks = tuple(stacks)
            if tuple(stacks) in dictionary:
                return dictionary[tupStacks]
            else:
                stacks[i] -= num
                flag = canWinNimMemRec(stacks, dictionary)
                stacks[i] += num
                dictionary[tupStacks] = not flag
                if not flag:
                    return True
    return False


############
# QUESTION 3
############

# A function to print nested lists as matrices row by row
def print_mat(mat):
    n = len(mat)
    for i in range(n):
        print(mat[i])


def concat_hor(mat1, mat2):
    pass  # replace with your code


def concat_vert(mat1, mat2):
    pass  # replace with your code


def inv(mat):
    pass  # replace with your code


def had(n):
    pass  # replace with your code


############
# QUESTION 4
############
def subset_sum_search(L, s):
    pass  # replace with your code


############
# QUESTION 6
############

def comp(s1, s2):
    pass  # replace with your code


def comp_ext(s1, s2):
    pass  # replace with your code


########
# Tester
########

def test():
    if not can_win_nim([3, 1, 1]):
        print("Error in can_win_nim")

    if can_win_nim([3, 2, 1]):
        print("Error in can_win_nim")

    if not can_win_nim([7]):
        print("Error in can_win_nim")

    if not can_win_nim_mem([3, 1, 1]):
        print("Error in can_win_nim_mem")

    if can_win_nim_mem([3, 2, 1]):
        print("Error in can_win_nim_mem")

    if not can_win_nim_mem([7]):
        print("Error in can_win_nim_mem")

    if had(0) != [[0]]:
        print("Error in had")

    if had(2) != [[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 1], [0, 1, 1, 0]]:
        print("Error in had")

    contains = lambda L, R: all(R.count(r) <= L.count(r) for r in R)
    L = [1, 2, 4, 8, 16]

    R = subset_sum_search(L, 13)
    if R == None or not sum(R) == 13 or not contains(L, R):
        print("Error in subset_sum_search")

    R = subset_sum_search(L, 32)
    if not R == None:
        print("Error in subset_sum_search")

    L = [i for i in range(1, 10)]
    R = subset_sum_search(L, 7)
    if R == None or not sum(R) == 7 or not contains(L, R):
        print("Error in subset_sum_search")

    if not comp("abc", "abc"):
        print("Error in comp")

    if comp("abc", "abcd"):
        print("Error in comp")

    if comp("", "abc"):
        print("Error in comp")

    if not comp_ext("abc+e", "abcde"):
        print("Error in comp_ext")

    if comp_ext("abc+", "abcdd"):
        print("Error in comp_ext")

    if not comp_ext("abc*d", "abcd"):
        print("Error in comp_ext")

    if not comp_ext("abc*d", "abcddd"):
        print("Error in comp_ext")

    if not comp_ext("a***", "a"):
        print("Error in comp_ext")

    if not comp_ext("abc+d*e", "abcxdzzzzzzzze"):
        print("Error in comp_ext")

    if comp_ext("abc+d*e", "abcdzzzze"):
        print("Error in comp_ext")

test()