from collections import deque

class MazSolver:
    def __init__(self, cells, entry, exit):
        self.cells = cells
        self.entry = entry
        self.exit = exec

    def solve(self):
        queue = deque([self.entry])
        visited = {self.entry}

        while queue:
            current = queue.popleft()
            if current == self.exit:
                # return stat later ####################
                break
