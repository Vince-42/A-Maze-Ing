*This project has been created as part of the 42 curriculum by Vleroy, Semirkar.*

# A-Maze-ing

## Description

A-Maze-ing is a Python maze-generation, solving, and terminal-visualization project developed by students of 42 Berlin. It reads maze parameters from `config.txt`, generates a maze with a blocked `42` motif, finds a shortest route between the entrance and exit, and writes a hexadecimal wall map to a text file.

The project is an independent student project, not an official product of 42 Berlin.

## Instructions

### Requirements and installation

- Python 3.10 or newer
- `make` and `pip`
- A terminal supporting ANSI colors and Unicode characters (for the intended visual presentation)

From the project root, run:

```bash
make install
```

This creates `.venv` and installs `flake8` and `mypy`. No third-party runtime Python packages are imported by the main application in the supplied source code.

### Running the project

```bash
make run
```

Alternatively, from the project root:

```bash
python3 a_maze_ing.py config.txt
```

The current entry-point code explicitly expects the argument `config.txt` and reads that file from the working directory.

Other Makefile targets:

| Command | Purpose |
| --- | --- |
| `make debug` | Run the application with Python's `pdb` debugger |
| `make lint` | Run `flake8` and `mypy` |
| `make clean` | Remove Python cache directories without deleting `.venv` |

## Configuration

The included `config.txt` contains:

```ini
WIDTH=15
HEIGHT=15
ENTRY=3,2
EXIT=14,9
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=6
```

| Key | Meaning |
| --- | --- |
| `WIDTH` | Maze width in cells |
| `HEIGHT` | Maze height in cells |
| `ENTRY` | Entrance coordinates (`x,y`) |
| `EXIT` | Exit coordinates (`x,y`) |
| `OUTPUT_FILE` | Destination for the generated wall map |
| `PERFECT` | `True` selects the perfect-maze generation branch; `False` selects the imperfect-maze branch |
| `SEED` | Optional integer seed for Python's random generator; the supplied configuration uses `6` |

Coordinates are zero-based. The configuration parser recognizes the keys above; the commented `algorithm` and `display mode` lines in `config.txt` are not currently active configuration options.

## Maze-generation algorithm

The generator is implemented in `core/maze_generator.py`. It creates a grid of cells and uses a **randomized depth-first search (recursive backtracker implemented with a stack)**:

1. Choose a random starting cell outside the blocked `42` motif.
2. Select a random unvisited neighboring cell.
3. Open the shared wall and mark the neighbor visited.
4. Backtrack when no unvisited neighbor remains.

This approach was selected because it is straightforward to implement with an explicit stack, supports randomized exploration, and naturally produces a connected, tree-like maze in perfect mode when all accessible cells are visited.

For `PERFECT=False`, the code runs a separate backtracking method and then `imperfect_helper()` to open additional connections and introduce loops. The code includes checks around the blocked `42` motif. These describe the implemented approach; the supplied ZIP does not contain automated test results proving every generated maze satisfies every subject constraint.

When `SEED` is present, `core/config.py` seeds Python's `random` module.

## Shortest-path solver

`core/maz_solver.py` implements **breadth-first search (BFS)** in `MazSolver`.

The solver uses a FIFO queue, a `visited` set, and a `came_from` dictionary. When the exit is reached, it reconstructs the shortest path as cell coordinates. `path_to_directions()` can convert a coordinate path to `N`, `E`, `S`, and `W` steps.

The maze generator invokes the solver after generation and marks the solution cells for optional terminal display.

## Terminal visualization and controls

The application uses Unicode block characters, emoji (including a snake for the entrance and an apple for the exit), and ANSI color sequences defined in `utils/design.py` and `utils/color.py`.

The interactive menu currently offers:

| Key | Action |
| --- | --- |
| `1` | Generate a new maze |
| `2` | Rotate wall color |
| `3` | Show or hide the solution |
| `4` | Print the maze's coordinate output in the terminal |
| `5` | Change the color/design of the `42` motif |
| `6` | Toggle perfect/imperfect mode (bonus menu option) |
| `7` | Change display speed |
| Any other key | Quit |

Display speed is set from the entered number divided by 10 and applied as a delay between printed rows. Emoji appearance depends on the terminal and font.

## Output file format

`core/maze_generator.py` writes one hexadecimal digit per cell, with one row per line. Each digit encodes four wall bits:

| Bit | Wall |
| --- | --- |
| 0 | North |
| 1 | East |
| 2 | South |
| 3 | West |

A set bit (`1`) indicates a closed wall; an unset bit (`0`) indicates an open passage. After the wall grid and a blank line, the current writer adds the entrance and exit coordinates on separate lines.

**Current limitation:** although the solver computes a shortest path, the supplied `print_data()` implementation does **not yet write the path-direction string** into the output file. This must be added before claiming full compliance with the subject's output format.

## Project structure

```text
A-Maze-ing/
├── a_maze_ing.py         # Application entry point and interactive menu
├── core/
│   ├── config.py         # Configuration parsing and validation
│   ├── maze_generator.py # Maze generation, rendering, and output
│   └── maz_solver.py     # BFS shortest-path solver
├── utils/
│   ├── color.py          # ANSI color constants
│   ├── design.py         # Terminal symbols and themes
│   └── error.py          # Custom exceptions
├── maze_analyzer.py      # Standalone maze-output analysis utility
├── config.txt            # Example configuration
├── Makefile
├── LICENSE.md
└── README.md
```

## Testing and code quality

Run the configured checks with:

```bash
make lint
```

The repository also includes `maze_analyzer.py`, a command-line utility for checking wall coherence and analyzing maze properties. Its documented usage is:

```bash
python3 maze_analyzer.py maze.txt
```

The analyzer also supports `--min-loops` and `--max-dead-ends` thresholds. Its presence does not by itself establish that all test cases pass. Test the generator with multiple dimensions, seeds, entrance/exit positions, and both values of `PERFECT`.

## Reusable maze module and packaging

The MazeGenerator class has to be instanciated with an object file that include the below variable :
obj._entry
obj._exit
obj._width
obj._height
obj._output_file
obj._perfect

Custom parameters can be shared via the `config.txt` file -> e.g Seeds

The maze structure can be printed on the terminal via `print_maze`
The solution can be printed if solution=True is passed to `print_maze`
The maze data can be accessed via `maze.txt` or `obj.output_txt`

## Team and project management

**Contributors:** Vleroy and Semirkar (42 Berlin).

The project work was divided as follows:

- **Vleroy:** maze generation (including perfect and imperfect maze logic) and terminal visualization.
- **Semirkar:** project structure, BFS maze solver, Makefile, Python virtual environment, `flake8` and `mypy` checks, and documentation.

### Collaboration and development process

Responsibilities were assigned at the beginning of the project to establish a clear development plan and enable parallel progress. Although each contributor had primary ownership of specific components, both team members supported one another throughout development, collaborating on technical challenges, integration, and improvements as needed.

The team used a shared GitHub repository with access for both contributors to manage source code, coordinate changes, and integrate their work. Slack served as the primary communication channel for sharing progress updates, communicating changes, and discussing emerging requirements throughout the project.

This approach combined clearly defined individual responsibilities with ongoing collaboration and communication.

### Reflection

The initial division of responsibilities helped the team work in parallel, while mutual support and regular Slack updates helped coordinate changes. One area for improvement would be to formalize integration milestones and maintain a shared checklist for end-to-end testing and packaging before submission.

## Resources

### References

- [Python documentation — `random`](https://docs.python.org/3/library/random.html): randomization and reproducible seeds.
- [Python documentation — `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque): FIFO queue operations used in BFS.
- [Python documentation — `venv`](https://docs.python.org/3/library/venv.html): Python virtual environments.
- [flake8 documentation](https://flake8.pycqa.org/): Python linting.
- [mypy documentation](https://mypy.readthedocs.io/): static type checking.

These are relevant technical references, not a claim that every source was consulted during implementation.

### Peer consultation and AI usage

The team also consulted fellow students at 42 Berlin to exchange ideas, discuss technical challenges, and strengthen their understanding of programming concepts.

Artificial intelligence tools were used sparingly during the development of this project, primarily as educational resources to clarify programming concepts, improve understanding of technical topics, and support independent learning.

AI assistance was limited mainly to clarifying programming concepts and understanding technical topics; it was not used as a substitute for the team's own implementation and review. Both contributors remained responsible for technical decisions, implementation, testing, and validation.

## License

Copyright (c) 2026 Vleroy and Semirkar.

Released under the MIT License. See [LICENSE.md](LICENSE.md). The project is provided without warranty, subject to applicable law.