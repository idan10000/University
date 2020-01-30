class Node():
    def __init__(self, val):
        self.value = val
        self.next = None

    def __repr__(self):
        # return "[" + str(self.value) + "," + str(id(self.next))+ "]"

        # for today's recitation, we print the id of self instead of self.next
        return "[" + str(self.value) + "," + str(id(self)) + "]"


class Linked_list():

    def __init__(self, seq=None):
        self.next = None
        self.len = 0
        if seq != None:
            for x in seq[::-1]:
                self.add_at_start(x)

    def __repr__(self):
        out = ""
        p = self.next
        while p != None:
            out += str(p) + " "  # str envokes __repr__ of class Node
            p = p.next
        return out

    def __len__(self):
        ''' called when using Python's len() '''
        return self.len

    def add_at_start(self, val):
        ''' add node with value val at the list head '''
        p = self
        tmp = p.next
        p.next = Node(val)
        p.next.next = tmp
        self.len += 1

    def add_at_end(self, val):
        ''' add node with value val at the list tail '''
        p = self
        while (p.next != None):
            p = p.next
        p.next = Node(val)
        self.len += 1

    def insert(self, loc, val):
        ''' add node with value val after location 0<=loc<len of the list '''
        assert 0 <= loc < len(self)
        p = self
        for i in range(0, loc):
            p = p.next
        tmp = p.next
        p.next = Node(val)
        p.next.next = tmp
        self.len += 1

    def __getitem__(self, loc):
        ''' called when using L[i] for reading
            return node at location 0<=loc<len '''
        assert 0 <= loc < len(self)
        p = self.next
        for i in range(0, loc):
            p = p.next
        return p

    def __setitem__(self, loc, val):
        ''' called when using L[loc]=val for writing
            assigns val to node at location 0<=loc<len '''
        assert 0 <= loc < len(self)
        p = self.next
        for i in range(0, loc):
            p = p.next
        p.value = val
        return None

    def find(self, val):
        ''' find (first) node with value val in list '''
        p = self.next
        # loc = 0     # in case we want to return the location
        while p != None:
            if p.value == val:
                return p
            else:
                p = p.next
                # loc=loc+1   # in case we want to return the location
        return None

    def delete(self, loc):
        ''' delete element at location 0<=loc<len '''
        assert 0 <= loc < len(self)
        p = self
        for i in range(0, loc):
            p = p.next
        # p is the element BEFORE loc
        p.next = p.next.next
        self.len -= 1