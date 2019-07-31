import numpy as np

class Node:
    def __init__(self, maxrow, maxcol, state=None):
        self.maxrow = maxrow
        self.maxcol = maxcol
        self.state = state

    def get_next_nodes(self):
        if self.state == None:
            return[(0, 0)]
        matrix = np.zeros((self.maxrow + 1, self.maxcol + 1), dtype=bool)
        matrix[0, :] = 1
        matrix[:, 0] = 1

        for tup in self.state:
            matrix[tup[0] + 1, tup[1] + 1] = 1

        candidates = []
        for i in range(1, self.maxrow + 1):
            for j in range(1, self.maxcol + 1):
                if (not matrix[i, j] and matrix[i - 1, j] and matrix[i, j - 1]):
                    candidates.append((i - 1, j - 1))
        
        next_nodes = []
        for candidate in candidates:
            next_node = list(self.state)
            next_node.append(candidate)
            next_node.sort()
            next_nodes.append(tuple(next_node))
        return next_nodes

    def get_childs(self, state):
        if state == None:
            return[(0, 0)]
        matrix = np.zeros((self.maxrow + 1, self.maxcol + 1), dtype=bool)
        matrix[0, :] = 1
        matrix[:, 0] = 1

        for tup in state:
            matrix[tup[0] + 1, tup[1] + 1] = 1

        candidates = []
        for i in range(1, self.maxrow + 1):
            for j in range(1, self.maxcol + 1):
                if (not matrix[i, j] and matrix[i - 1, j] and matrix[i, j - 1]):
                    candidates.append((i - 1, j - 1))
        
        next_nodes = []
        for candidate in candidates:
            next_node = list(state)
            next_node.append(candidate)
            next_node.sort()
            next_nodes.append(tuple(next_node))
        return next_nodes
    
    def get_all_children(self):
        children = set()
        this_children = self.get_next_nodes()
        while (this_children != []):
            this_children_set = set()
            for child in this_children:
                if child == (0, 0):
                    child = ((0, 0),)
                children.add(child)
                this_children_set = set(self.get_childs(child)) | this_children_set
            this_children = list(this_children_set)
        return children
        

