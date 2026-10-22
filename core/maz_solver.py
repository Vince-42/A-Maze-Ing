from collections import deque

class MazSolver:
    def __init__(self, cells, entry, exit):
        self.cells = cells
        self.entry = entry
        self.exit = exit
        self.cell_dict = {}
        for cell in cells:
            self.cell_dict[cell.coordinate] = cell

    def get_neighbers(
            self, current: tuple[int, int]
    ) -> list[tuple[int, int]]:
        x, y = current
        

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
