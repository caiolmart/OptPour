import numpy as np

class Node:
    def __init__(self, maxrow, maxcol, state=None):
        self.maxrow = maxrow
        self.maxcol = maxcol
        self.state = state

    def get_next_nodes(self):
        return self.get_children(self.state)

    def get_children(self, state):
        if state == None:
            return[((0, 0), )]
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
                this_children_set = set(self.get_children(child)) | \
                    this_children_set
            this_children = list(this_children_set)
        return children

    def array_from_state(self, state):
        matrix = np.zeros((self.maxrow, self.maxcol), dtype=bool)
        for tup in state:
            matrix[tup[0], tup[1]] = 1
        return matrix

    def eval_qtt(self, state, qtt_array):
        state_array = self.array_from_state(state)
        return np.sum(np.multiply(state_array, qtt_array))

    def eval_br(self, state, qtt_array, bad_array):
        total = self.eval_qtt(state, qtt_array)
        bad = self.eval_qtt(state, bad_array)
        return bad / total

    def optimize_naive(self, qtt_array, bad_array, br_threshold, 
                       only_in_thresh=True):
        all_states = self.get_all_children()
        candidates = dict()
        for state in all_states:
            br = self.eval_br(state, qtt_array, bad_array)
            qtt = self.eval_qtt(state, qtt_array)
            if br <= br_threshold:
                in_thresh = 1
            else:
                in_thresh = 0
            candidates[state] = (in_thresh, qtt, br)
        sorted_candidates = sorted(candidates.items(), 
                                   key=lambda x: (x[1][0], x[1][1], -x[1][2]),
                                   reverse=True)
        if only_in_thresh:
            only_in = [x for x in sorted_candidates if x[1][0] == 1]
            return only_in
        else:
            return sorted_candidates