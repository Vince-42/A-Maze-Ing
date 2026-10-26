from collections import deque

class MazSolver:
    def __init__(self, cells, entry, exit):
        self.cells = cells
        self.entry = entry
        self.exit = exit
        self.cell_dict = {}
        for cell in cells:
            self.cell_dict[cell.coordinate] = cell

    """
    Find all accessible neighbors of the current cell.
    """
    def get_neighbors(
            self, current: tuple[int, int]
    ) -> list[tuple[int, int]]:
        
        x, y = current
        neighbors: list[tuple[int, int]] = []
        cell = self.cell_dict[current]

        if cell.stateN:
            if  (x, y - 1) in self.cell_dict and not self.cell_dict[x, y - 1].fortytwo:
                neighbors.append((x, y - 1))
        if cell.stateE:
            if (x + 1, y) in self.cell_dict and not self.cell_dict[x + 1, y].fortytwo:
                neighbors.append((x + 1, y))
        if cell.stateS:
            if (x, y + 1) in self.cell_dict and not self.cell_dict[x, y + 1].fortytwo:
                neighbors.append((x, y + 1))

        if cell.stateW:
            if (x - 1, y) in self.cell_dict and not self.cell_dict[x - 1, y].fortytwo:
                neighbors.append((x - 1, y))

        return neighbors
        

    def build_path(self, parent):
        pass


    def solve(self):
        queue = deque([self.entry])
        visited = {self.entry}
        came_from = {self.entry: None}

        while queue:
            current = queue.popleft()
            if current == self.exit:
                # return stat later ####################
                break

        current_cell = self.cell_dict[current]
