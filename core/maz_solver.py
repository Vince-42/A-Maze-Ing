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
            if  (x, y - 1) in self.cell_dict and not self.cell_dict[x, y - 1].blocked:
                neighbors.append((x, y - 1))
        if cell.stateE:
            if (x + 1, y) in self.cell_dict and not self.cell_dict[x + 1, y].blocked:
                neighbors.append((x + 1, y))
        if cell.stateS:
            if (x, y + 1) in self.cell_dict and not self.cell_dict[x, y + 1].blocked:
                neighbors.append((x, y + 1))

        if cell.stateW:
            if (x - 1, y) in self.cell_dict and not self.cell_dict[x - 1, y].blocked:
                neighbors.append((x - 1, y))

        return neighbors


    """Build path backwards,
    from exit to entry, then return reverse"""
    def build_path(self, came_from):
        path: list[tuple[int, int]] = []
        current = self.exit

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path

        
    """
    Find the shortest path using BFS.
    Return path as a list of coordinates,
    or an empty list if no path exists.
    """
    def solve(self):
        queue = deque([self.entry])
        visited = {self.entry}
        came_from = {self.entry: None}

        while queue:
            current = queue.popleft()
            if current == self.exit:
                break

            for neighb in self.get_neighbors(current):
                if neighb not in visited:
                    visited.add(neighb)
                    came_from[neighb] = current
                    queue.append(neighb)

        if self.exit not in came_from:
            return []
        
        return self.build_path(came_from)


        """
        Convert solution path into a string of
        N, E, S, W directions
        """
    def path_to_directions(
            self, path: list[tuple[int, int]]
    ) -> str:
        
        directions = ""

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            if x2 > x1:
                directions += 'E'
            elif x2 < x1:
                directions += 'W'
            elif y2 > y1:
                directions += 'S'
            elif y2 < y1:
                directions += 'N'

        return directions
        

