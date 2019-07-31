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
