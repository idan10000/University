import time
import sys


############
# QUESTION 2
############
def can_win_nim(stacks):
    if len([0 for stack in stacks if stack != 0]) == 1:
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
    d = {tuple([0 for i in range(len(stacks))]): False}
    return canWinNimMemRec(stacks, d)


def canWinNimMemRec(stacks, dictionary):
    if len([0 for stack in stacks if stack != 0]) == 1:
        return True
    tupStacks = tuple(sorted(stacks))
    if tupStacks in dictionary:
        return dictionary[tupStacks]
    for i in range(len(stacks)):
        for num in range(1, stacks[i] + 1):
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
    mergedList = list()
    for i in range(len(mat1)):
        mergedList.append(mat1[i] + mat2[i])
    return mergedList


def concat_vert(mat1, mat2):
    mergedList = list()
    for item in mat1:
        mergedList.append(item)
    for item in mat2:
        mergedList.append(item)
    return mergedList


def inv(mat):
    newMat = list()
    for row in mat:
        newRow = list()
        for i in range(len(row)):
            newRow.append(1 - row[i])
        newMat.append(newRow)
    return newMat


def had(n):
    if n == 0:
        return [[0]]
    lastMat = had(n - 1)
    newMat = concat_vert(concat_hor(lastMat, lastMat), concat_hor(lastMat, inv(lastMat)))
    return newMat


############
# QUESTION 4
############
def subsetSumSearchRec(L, s, dictionary):
    if L == [] or s <= 0:
        return None
    if L[0] - s == 0:
        return [L[0]]
    tempTup = tuple([tuple(L), s])
    if tempTup in dictionary:
        return dictionary[tempTup]
    else:
        newList = L[1:]
        withFirst = subsetSumSearchRec(newList, s-L[0], dictionary)
        dictionary[tuple([tuple(newList), s-L[0]])] = withFirst
        if withFirst is not None:
            withFirst.append(L[0])
            return withFirst
        else:
            withoutFirst = subsetSumSearchRec(newList, s, dictionary)
            dictionary[tuple([tuple(newList), s])] = withoutFirst
            if withoutFirst is not None:
                return withoutFirst




def subset_sum_search(L, s):
    dictionary = {}
    return subsetSumSearchRec(L, s, dictionary)



############
# QUESTION 6
############

def comp(s1, s2):
    if len(s1) is 0 and len(s2) is 0:
        return True
    if len(s1) != len(s2) or s1[0] != s2[0]:
        return False
    return comp(s1[1:], s2[1:])

def comp_ext(s1, s2):
    if len(s1) == 0 and len(s2) != 0:
        return False
    if len(s1) is 0 and len(s2) is 0:
        return True
    if s1[-1] == '+':
        return comp_ext(s1[:-1], s2[:-1])
    if s1[-1] == '*':
        return comp_ext(s1[:-1], s2[:len(s1)-1])
    if s1[-1] == s2[-1]:
        return comp_ext(s1[:-1], s2[:-1])
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
