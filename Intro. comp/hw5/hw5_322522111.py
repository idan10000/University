import copy
import random
import string
import time


############
# QUESTION 1
############

class SparseMatrix:
    """
    Represents a rectangular matrix with n rows and m columns.
    """

    def __init__(self, n, m):
        """
        Create an n-by-m matrix of val's.
        Inner representation: list of lists (rows)
        """
        assert n > 0 and m > 0
        self.rows = {}
        self.size = (n, m)

    def __repr__(self):
        s = ""
        for i in range(self.dim()[0]):
            l = []
            if i not in self.rows:
                l = [0 for j in range(self.dim()[1])]
            else:
                for j in range(self.dim()[1]):
                    if j in self.rows[i]:
                        l.append(self.rows[i][j])
                    else:
                        l.append(0)

            s += str(l) + "\n"

        return s

    def dim(self):
        return self.size

    def __eq__(self, other):
        assert isinstance(other, SparseMatrix)
        return self.rows == other.rows and self.size == other.size

    def __getitem__(self, ij):  # ij is a tuple (i,j). Allows m[i,j] instead m[i][j]
        if ij[0] > self.size[0] or ij[1] > self.size[1]:
            return "index out of bounds"
        if ij[0] in self.rows:
            if ij[1] in self.rows[ij[0]]:
                return self.rows[ij[0]][ij[1]]
        return 0

    def __setitem__(self, ij, val):  # ij is a tuple (i,j). Allows m[i,j] instead m[i][j]
        if ij[0] >= self.size[0] or ij[1] >= self.size[1]:
            return "index out of bounds"
        if val != 0:
            if ij[0] in self.rows:
                self.rows[ij[0]][ij[1]] = val
            else:
                self.rows[ij[0]] = {ij[1]: val}
        elif ij[0] in self.rows:
            self.rows[ij[0]].pop(ij[1], None)

    def __add__(self, other):
        assert self.size == other.size and isinstance(other, SparseMatrix)
        sum = copy.deepcopy(self.rows)
        for row in other.rows:
            if row in sum:
                for col in other.rows[row]:
                    if col in sum[row]:
                        sum[row][col] += other.rows[row][col]
                        if sum[row][col] == 0:
                            if len(sum[row]) == 1:
                                del sum[row]
                            else:
                                del sum[row][col]
                    else:
                        sum[row][col] = other.rows[row][col]
            else:
                sum[row] = copy.copy(other.rows[row])
        mat = SparseMatrix(self.size[0], self.size[1])
        mat.rows = sum
        return mat

    def __neg__(self):
        newMat = copy.deepcopy(self.rows)
        for row in newMat:
            for item in newMat[row]:
                newMat[row][item] *= -1
        mat = SparseMatrix(self.size[0], self.size[1])
        mat.rows = newMat
        return mat

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        assert isinstance(other, SparseMatrix)
        assert self.dim()[1] == other.dim()[0]

        n, m = self.dim()[0], other.dim()[1]
        new = SparseMatrix(n, m)

        # create columns dict for other
        other_cols = {}
        for i in other.rows:
            for j in other.rows[i]:
                if j not in other_cols:
                    other_cols[j] = {}
                other_cols[j][i] = other.rows[i][j]

        for i in self.rows:
            for j in other_cols:
                s_ij = 0
                row = self.rows[i]
                for k in self.rows[i]:
                    if k in other_cols[j]:
                        s_ij += self.rows[i][k] * other_cols[j][k]
                if s_ij != 0:
                    if i not in new.rows:
                        new.rows[i] = {}
                    new.rows[i][j] = s_ij

        return new


# These functions are not part of the class

def mat2a():
    mat = SparseMatrix(1, 3)
    mat[0, 0] = 6
    mat[0, 1] = 1
    mat[0, 2] = 3
    return mat


def mat2b():
    return None


def mat2c():
    mat = SparseMatrix(1, 7)
    mat[0, 7] = 10
    return mat


############
# QUESTION 2
############

def printree(t, bykey=True):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    # for row in trepr(t, bykey):
    #        print(row)
    return trepr(t, bykey)


def trepr(t, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if t == None:
        return ["#"]

    thistr = str(t.key) if bykey else str(t.val)

    return conc(trepr(t.left, bykey), thistr, trepr(t.right, bykey))


def conc(left, root, right):
    """Return a concatenation of textual represantations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "|" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result


def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1


def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i


class Tree_node():
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return "(" + str(self.key) + ":" + str(self.val) + ")"


class Binary_search_tree():

    def __init__(self):
        self.root = None

    def __repr__(self):  # no need to understand the implementation of this one
        out = ""
        for row in printree(self.root):  # need printree.py file
            out = out + row + "\n"
        return out

    def lookup(self, key):
        ''' return node with key, uses recursion '''

        def lookup_rec(node, key):
            if node == None:
                return None
            elif key == node.key:
                return node
            elif key < node.key:
                return lookup_rec(node.left, key)
            else:
                return lookup_rec(node.right, key)

        return lookup_rec(self.root, key)

    def insert(self, key, val):
        ''' insert node with key,val into tree, uses recursion '''

        def insert_rec(node, key, val):
            if key == node.key:
                node.val = val  # update the val for this key
            elif key < node.key:
                if node.left == None:
                    node.left = Tree_node(key, val)
                else:
                    insert_rec(node.left, key, val)
            else:  # key > node.key:
                if node.right == None:
                    node.right = Tree_node(key, val)
                else:
                    insert_rec(node.right, key, val)
            return

        if self.root == None:  # empty tree
            self.root = Tree_node(key, val)
        else:
            insert_rec(self.root, key, val)

    def minimum(self):
        ''' return node with minimal key '''
        if self.root == None:
            return None
        node = self.root
        left = node.left
        while left != None:
            node = left
            left = node.left
        return node

    def depth(self):
        ''' return depth of tree, uses recursion'''

        def depth_rec(node):
            if node == None:
                return -1
            else:
                return 1 + max(depth_rec(node.left), depth_rec(node.right))

        return depth_rec(self.root)

    def size(self):
        ''' return number of nodes in tree, uses recursion '''

        def size_rec(node):
            if node == None:
                return 0
            else:
                return 1 + size_rec(node.left) + size_rec(node.right)

        return size_rec(self.root)

    def max_sum(self):
        def maxSumRec(node):
            if node is None:
                return 0
            return node.val + max(maxSumRec(node.left), maxSumRec(node.right))

        return maxSumRec(self.root)

    def is_balanced(self):
        def isBalancedRec(node):  # returns tuple = (bool isBalanced, max depth)
            if node is None:
                return True, 0
            left = isBalancedRec(node.left)
            right = isBalancedRec(node.right)
            return abs(left[1] - right[1]) <= 1, max(left[1], right[1]) + 1

        return isBalancedRec(self.root)[0]

    def diam(self):
        def diamRec(node):  # returns tuple = (max diam, max depth)
            if node is None:
                return 0, 0
            left = diamRec(node.left)
            right = diamRec(node.right)
            return max(left[0], right[0], (left[1] + right[1] + 1)), max(left[1], right[1]) + 1

        return diamRec(self.root)[0]


############
# QUESTION 3
############

class Node():

    def __init__(self, val):
        self.value = val
        self.next = None
        self.prev = None

    def __repr__(self):
        return str(self.value) + "(" + str(id(self)) + ")"
    # This shows pointers as well for educational purposes


class DLList():

    def __init__(self, seq=None):
        self.head = None
        self.tail = None
        self.len = 0
        if seq != None:
            for item in seq:
                self.insert(item)

    def __len__(self):
        return self.len

    def __repr__(self):
        out = ""
        p = self.head
        while p != None:
            out += str(p) + ", "  # str(p) envokes __repr__ of class Node
            p = p.next
        return "[" + out[:-2] + "]"

    def insert(self, val, first=False):
        newNode = Node(val)
        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            if first:
                self.head.prev, self.head, newNode.next, = newNode, newNode, self.head
            else:
                tail = self.tail
                tail.next = newNode
                newNode.prev = tail
                self.tail = newNode
        self.len += 1

    def reverse(self):
        node = self.tail
        node.next, node.prev = node.prev, node.next
        node = node.next
        if node is not None:
            while node is not None:
                node.next, node.prev = node.prev, node.next
                node = node.next
            self.head, self.tail = self.tail, self.head

    def rotate(self, k):
        if self.len - k > k:
            tempNode = self.tail
            for i in range(k - 1):
                tempNode = tempNode.prev
            newTail = tempNode.prev
            tempNode.prev.next, tempNode.prev = None, None
            self.tail.next, self.head.prev = self.head, self.tail
            self.head = tempNode
            self.tail = newTail
        else:
            tempNode = self.head
            for i in range(self.len - k - 1):
                tempNode = tempNode.next
            tempNode.next.prev = None
            self.tail.next = self.head
            self.head.prev = self.tail
            self.head = tempNode.next
            tempNode.next, self.tail = None, tempNode

    def delete_node(self, node):
        if node is self.head:
            self.head = node.next
        else:
            node.prev.next = node.next
        if node is self.tail:
            self.tail = node.prev
        else:
            node.next.prev = node.prev
        self.len -= 1


############
# QUESTION 5
############
# a
def substr_overlap(lst, k):
    out = list()
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            for a in range(len(lst[i]) - k + 1):
                s_a = lst[i][a:a + k]
                for b in range(len(lst[j]) - k + 1):
                    if s_a == lst[j][b:b + k]:
                        out.append((i, j, a, b))
    return out


# c
#########################################
### Dict class ###
#########################################

class Dict:
    def __init__(self, m, hash_func=hash):
        """ initial hash table, m empty entries """
        self.table = [[] for i in range(m)]
        self.hash_mod = lambda x: hash_func(x) % m

    def __repr__(self):
        L = [self.table[i] for i in range(len(self.table))]
        return "".join([str(i) + " " + str(L[i]) + "\n" for i in range(len(self.table))])

    def insert(self, key, value):
        """ insert key,value into table
            Allow repetitions of keys """
        i = self.hash_mod(key)  # hash on key only
        item = [key, value]  # pack into one item
        self.table[i].append(item)

    def find(self, key):
        """ returns ALL values of key as a list, empty list if none """
        hashedKey = self.hash_mod(key)
        return [lst[1] for lst in self.table[hashedKey] if lst[0] == key]


#########################################
### End Dict class ###
#########################################

# d
def substr_overlap_hash1(lst, k):
    strDict = Dict(len(lst)**2)
    out = list()

    for i in range(len(lst) - 1, -1, -1):
        for a in range(len(lst[i]) - k + 1):
            s_a = lst[i][a:a + k]
            vals = strDict.find(s_a)
            for val in vals:
                if val[0] != i:
                    out.append((i, val[0], a, val[1]))
            strDict.insert(s_a, (i, a))
    return out

# f
def substr_overlap_hash2(lst, k):
    strDict = {}
    out = list()

    for i in range(len(lst) - 1, -1, -1):
        for a in range(len(lst[i]) - k + 1):
            s_a = lst[i][a:a + k]
            if s_a in strDict:
                vals = strDict[s_a]
                for val in vals:
                    if val[0] != i:
                        out.append((i, val[0], a, val[1]))
                strDict[s_a].append((i, a))
            else:
                strDict[s_a] = [(i, a)]
    return out


########
# Tester
########

def test():
    # Testing Q1
    m = SparseMatrix(3, 2)
    m1 = SparseMatrix(3, 2)
    if m != m1:
        print("error in SparseMatrix.__eq__ll")
    m[1, 0] = 30
    m[2, 1] = -2
    x = m[1, 1]
    y = m[2, 1]
    if (x != 0 or y != -2):
        print("error in SparseMatrix.__getitem__ or SparseMatrix.__setitem__")
    if m.__repr__() != "[0, 0]\n[30, 0]\n[0, -2]\n":
        print("error in SparseMatrix.__repr__")
    if m.dim() != (3, 2):
        print("error in SparseMatrix.dim")
    m2 = SparseMatrix(3, 2)
    m2[0, 0] = 100
    m3 = m + m2
    if not isinstance(m3, SparseMatrix):
        print("error in SparseMatrix.__add__")
    elif m3[0, 0] != 100 or m3[2, 1] != -2:
        print("error in SparseMatrix.__add__")
    if m.__repr__() != "[0, 0]\n[30, 0]\n[0, -2]\n":
        print("error in SparseMatrix.__repr__ or SparseMatrix.__add__")
    m4 = m - m2
    if not isinstance(m4, SparseMatrix):
        print("error in SparseMatrix.__sub__")
    elif m4[0, 0] != -100 or m4[2, 1] != -2:
        print("error in SparseMatrix.__sub__")
    m4 = m - m
    if not isinstance(m4, SparseMatrix):
        print("error in SparseMatrix.__sub__")
    elif m4[0, 0] != 0 or m4[2, 1] != 0 or len(m4.rows) != 0:
        print("error in SparseMatrix.__sub__")
    m5 = -m
    if not isinstance(m5, SparseMatrix):
        print("error in SparseMatrix.__neg__")
    elif m5[1, 0] != -30 or m4[0, 1] != 0:
        print("error in SparseMatrix.__neg__")

    # Testing Q2
    # Question 2
    t = Binary_search_tree()
    if t.max_sum() != 0:
        print("error in Binary_search_tree.max_sum")
    t.insert('e', 1)
    t.insert('b', 2)
    if t.max_sum() != 3:
        print("error in Binary_search_tree.max_sum")
    t.insert('a', 8)
    t.insert('d', 4)
    t.insert('c', 10)
    t.insert('i', 3)
    t.insert('g', 5)
    t.insert('f', 7)
    t.insert('h', 9)
    t.insert('j', 6)
    t.insert('k', 5)
    if (t.max_sum() != 18):
        print("error in Binary_search_tree.max_sum")

    t = Binary_search_tree()
    if t.is_balanced() != True:
        print("error in Binary_search_tree.is_balanced")
    t.insert("b", 10)
    t.insert("d", 10)
    t.insert("a", 10)
    t.insert("c", 10)
    if t.is_balanced() != True:
        print("error in Binary_search_tree.is_balanced")
    t.insert("e", 10)
    t.insert("f", 10)
    if t.is_balanced() != False:
        print("error in Binary_search_tree.is_balanced")

    t2 = Binary_search_tree()
    t2.insert('c', 10)
    t2.insert('a', 10)
    t2.insert('b', 10)
    t2.insert('g', 10)
    t2.insert('e', 10)
    t2.insert('d', 10)
    t2.insert('f', 10)
    t2.insert('h', 10)
    if t2.diam() != 6:
        print("error in Binary_search_tree.diam")

    t3 = Binary_search_tree()
    t3.insert('c', 1)
    t3.insert('g', 3)
    t3.insert('e', 5)
    t3.insert('d', 7)
    t3.insert('f', 8)
    t3.insert('h', 6)
    t3.insert('z', 6)
    if t3.diam() != 5:
        print("error in Binary_search_tree.diam")

    # Testing Q3
    lst = DLList("abc")
    a = lst.head
    if a == None or a.next == None or a.next.next == None:
        print("error in DLList.insert")
    else:
        b = lst.head.next
        c = lst.tail
        if lst.tail.prev != b or b.prev != a or a.prev != None:
            print("error in DLList.insert")

    lst.insert("d", True)
    if len(lst) != 4 or lst.head.value != "d":
        print("error in DLList.insert")

    prev_head_id = id(lst.head)
    lst.reverse()
    if id(lst.tail) != prev_head_id or lst.head.value != "c" or lst.head.next.value != "b" or lst.tail.value != "d":
        print("error in DLList.reverse")

    lst.rotate(1)
    if lst.head.value != "d" or lst.head.next.value != "c" or lst.tail.value != "a":
        print("error in DLList.rotate")
    lst.rotate(3)
    if lst.head.value != "c" or lst.head.next.value != "b" or lst.tail.prev.value != "a":
        print("error in DLList.rotate")

    lst.delete_node(lst.head.next)
    if lst.head.next != lst.tail.prev or len(lst) != 3:
        print("error in DLList.delete_node")
    lst.delete_node(lst.tail)
    if lst.head.next != lst.tail or len(lst) != 2:
        print("error in DLList.delete_node")

    # Question 5
    s0 = "aaac"
    s1 = "caaaab"
    s2 = "edcaac"
    lst = [s0, s1, s2]
    k = 3
    if sorted(substr_overlap(lst, k)) != sorted([(0, 1, 0, 1), (0, 1, 0, 2), (1, 2, 0, 2), (0, 2, 1, 3)]):
        print("error in substr_overlap")

    d = Dict(3)
    d.insert(56, "a")
    d.insert(56, "b")
    if sorted(d.find(56)) != ["a", "b"] or d.find(34) != []:
        print("error in Dict.find")

    if sorted(substr_overlap_hash1(lst, k)) != sorted([(0, 1, 0, 1), (0, 1, 0, 2), (1, 2, 0, 2), (0, 2, 1, 3)]):
        print("error in substr_overlap_hash1")
    if sorted(substr_overlap_hash2(lst, k)) != sorted([(0, 1, 0, 1), (0, 1, 0, 2), (1, 2, 0, 2), (0, 2, 1, 3)]):
        print("error in substr_overlap_hash2")


def randomString(n):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(n))


def generateList(stringLen, numStrings):
    lst = list()
    for i in range(numStrings):
        lst.append(randomString(stringLen))
    return lst


