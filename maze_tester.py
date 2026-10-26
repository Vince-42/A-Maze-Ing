#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# noqa: SIZE_OK — one drop-in script by design; ~90 lines are the scenario data table

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Copy this script next to your maze program and run:
#      uv run maze_tester.py [--verbose]
#    Plain python3 works too — the script is stdlib-only:
#      python3 maze_tester.py
#    It defaults to ./a_maze_ing.py; override with a path argument:
#      python3 maze_tester.py ../elsewhere/a_maze_ing.py
#    or via env var:  MAZE_MAIN=../elsewhere/a_maze_ing.py python3 maze_tester.py
# 3. Exit code: 0 = every scenario behaved as expected, 1 = at least one did not.
# ──────────────────

"""Black-box scenario tester for the Amazing maze generator.

Contract assumed with the program under test (adjust the constants if yours
differs):

* invoked as ``python3 a_maze_ing.py <config-file>``;
* valid config -> exit code 0, no Python traceback, and OUTPUT_FILE is written
  as a grid of hex digits — one digit per cell, each digit encoding the cell's
  walls (see WALL_BITS) — followed by a blank line and the entry/exit
  coordinates, one "x, y" pair per line;
* invalid config -> no output maze and either a non-zero exit code or a clear
  error message — never an uncaught traceback, never a hang.

Coordinates are (x, y) and the config keys follow them: HEIGHT is the size
along x (grid columns), WIDTH the size along y (grid rows) — verified against
the shipped maze.txt example. A cell value of 0xF marks a blocked cell that is
excluded from the maze. Border walls must be closed everywhere, except that
the ENTRY and EXIT cells may open to the outside as doors.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, assert_never

TIMEOUT_S: Final = 55.0
HEX_RE: Final = re.compile(r"[0-9A-Fa-f]+")
COORDS_RE: Final = re.compile(r"^\s*(-?\d+)\s*,\s*(-?\d+)\s*$")
ERROR_MESSAGE_RE: Final = re.compile(
    r"\b(?:error|invalid|missing|failed|failure|wrong|negative|outside)\b"
    r"|\b(?:cannot|can't|can not|not found|no maze)\b",
    re.IGNORECASE,
)

# Wall bit of each direction inside one hex digit. Adjust to your format.
WALL_BITS: Final = {"N": 1, "E": 2, "S": 4, "W": 8}

# A cell whose value is 0xF is blocked: it is not part of the maze and its
# neighbours carry open walls toward it (verified against the shipped maze.txt).
BLOCKED: Final = 0xF

# (dx, dy, this cell's wall side, the neighbour's opposite side)
_DIRS: Final = ((0, -1, "N", "S"), (1, 0, "E", "W"), (0, 1, "S", "N"), (-1, 0, "W", "E"))

# Mirrors the config.txt shipped with the project.
BASE_CONFIG: Final = {
    "HEIGHT": "20",
    "WIDTH": "15",
    "ENTRY": "5,0",
    "EXIT": "9,9",
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": "False",
    "SEED": "None",
}

Grid = list[list[int]]


@dataclass(frozen=True, slots=True)
class Case:
    """One scenario: a config to feed the program and the expected behaviour."""

    name: str
    config: dict[str, str] | None  # None -> the config file must not exist
    expect_success: bool
    raw: str | None = None  # verbatim file content, takes precedence over config
    twice: Literal["stable", "varies"] | None = None  # run twice, compare outputs
    note: str = ""  # hint printed when the case fails


@dataclass(frozen=True, slots=True)
class RunOutcome:
    """What one invocation of the program produced."""

    returncode: int | None  # None -> the run timed out
    stdout: str
    stderr: str
    maze_text: str | None  # content of OUTPUT_FILE, None if not written


@dataclass(frozen=True, slots=True)
class MazeSpec:
    """Expected maze properties; HEIGHT = size along x, WIDTH = size along y."""

    x_size: int
    y_size: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    perfect: bool


@dataclass(frozen=True, slots=True)
class CaseResult:
    case: Case
    problems: tuple[str, ...]
    first: RunOutcome


def render_config(config: dict[str, str]) -> str:
    return "".join(f"{key}={value}\n" for key, value in config.items())


def parse_config_text(text: str) -> dict[str, str]:  # noqa: DICT_OK — open-ended keys by design
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        out[key.strip()] = value.strip()
    return out


def fed_config_text(case: Case) -> str:
    if case.raw is not None:
        return case.raw
    if case.config is None:
        return ""
    return render_config(case.config)


def parse_spec(cfg: dict[str, str]) -> MazeSpec | str:  # noqa: DICT_OK — boundary parse
    """Build the expected spec, or return an error message (harness-side bug)."""
    try:
        x_size = int(cfg["HEIGHT"])
        y_size = int(cfg["WIDTH"])
        entry_x, entry_y = (int(v) for v in cfg["ENTRY"].split(","))
        exit_x, exit_y = (int(v) for v in cfg["EXIT"].split(","))
    except (KeyError, ValueError) as exc:
        return f"harness could not parse its own config values: {exc}"
    return MazeSpec(x_size, y_size, (entry_x, entry_y), (exit_x, exit_y), cfg.get("PERFECT") == "True")


def run_program(main_py: Path, case: Case, workdir: Path) -> RunOutcome:
    """Run the program once inside a fresh directory and capture everything."""
    config_path = workdir / "config.txt"
    if case.config is not None:
        config_path.write_text(fed_config_text(case), encoding="utf-8")
    try:
        proc = subprocess.run(
            [sys.executable, str(main_py), config_path.name],
            cwd=workdir,
            input="7\n",  # Quit the interactive menu after the maze is generated.
            capture_output=True,
            text=True,
            timeout=TIMEOUT_S,
        )
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout if isinstance(exc.stdout, str) else ""
        err = exc.stderr if isinstance(exc.stderr, str) else ""
        return RunOutcome(None, out, err, None)
    out_name = (case.config or {}).get("OUTPUT_FILE", "maze.txt")
    maze_text: str | None = None
    if out_name:
        maze_file = workdir / out_name
        if maze_file.is_file():
            maze_text = maze_file.read_text(encoding="utf-8", errors="replace")
    return RunOutcome(proc.returncode, proc.stdout, proc.stderr, maze_text)


def extract_grid(text: str, cols: int, rows: int) -> Grid | None:
    """Locate the block of `rows` hex lines of `cols` digits in the output file."""
    hex_rows = [
        compact
        for line in text.splitlines()
        if (compact := line.replace(" ", "").strip().upper()) and HEX_RE.fullmatch(compact)
    ]
    for start in range(len(hex_rows) - rows + 1):
        window = hex_rows[start : start + rows]
        if all(len(row) == cols for row in window):
            return [[int(ch, 16) for ch in row] for row in window]
    return None


def has_wall(cell: int, side: str) -> bool:
    return bool(cell & WALL_BITS[side])


def maze_failures(grid: Grid, spec: MazeSpec) -> list[str]:
    """Structural checks: neighbour wall agreement and closed borders."""
    problems: list[str] = []
    doors = {spec.entry, spec.exit}
    for y in range(spec.y_size):
        for x in range(spec.x_size):
            if grid[y][x] == BLOCKED:
                continue
            for dx, dy, side, opposite in _DIRS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < spec.x_size and 0 <= ny < spec.y_size:
                    if grid[ny][nx] != BLOCKED and has_wall(grid[y][x], side) != has_wall(grid[ny][nx], opposite):
                        problems.append(f"wall disagreement at ({x},{y}) side {side}")
                elif (x, y) not in doors and not has_wall(grid[y][x], side):
                    problems.append(f"open border wall at ({x},{y}) side {side}")
                if len(problems) >= 5:
                    return problems
    return problems


def reachable(grid: Grid, spec: MazeSpec) -> set[tuple[int, int]]:
    """Every passable cell reachable from ENTRY through open walls (BFS)."""
    seen = {spec.entry}
    stack = [spec.entry]
    while stack:
        x, y = stack.pop()
        for dx, dy, side, _ in _DIRS:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < spec.x_size
                and 0 <= ny < spec.y_size
                and (nx, ny) not in seen
                and grid[ny][nx] != BLOCKED
                and not has_wall(grid[y][x], side)
            ):
                seen.add((nx, ny))
                stack.append((nx, ny))
    return seen


def trailer_problems(text: str, spec: MazeSpec) -> list[str]:
    """The output file must end with the entry and exit coordinate lines."""
    coords = [(int(m.group(1)), int(m.group(2))) for line in text.splitlines() if (m := COORDS_RE.match(line))]
    problems: list[str] = []
    if len(coords) < 2:
        return ["output file is missing the entry/exit coordinate lines"]
    if coords[0] != spec.entry:
        problems.append(f"entry line {coords[0]} does not match config ENTRY {spec.entry}")
    if coords[1] != spec.exit:
        problems.append(f"exit line {coords[1]} does not match config EXIT {spec.exit}")
    return problems


def success_problems(case: Case, outcome: RunOutcome) -> list[str]:
    """Everything a valid config must satisfy beyond exiting 0."""
    if outcome.returncode != 0:
        return [f"exit code {outcome.returncode} on a valid config"]
    if outcome.maze_text is None:
        return ["no output file was written"]
    match parse_spec(parse_config_text(fed_config_text(case))):
        case str() as err:
            return [err]
        case MazeSpec() as spec:
            pass
        case unreachable:
            assert_never(unreachable)
    grid = extract_grid(outcome.maze_text, spec.x_size, spec.y_size)
    if grid is None:
        return [f"no {spec.y_size}x{spec.x_size} hex grid found in the output file"]
    problems = trailer_problems(outcome.maze_text, spec)
    for label, (cx, cy) in (("ENTRY", spec.entry), ("EXIT", spec.exit)):
        if not (0 <= cx < spec.x_size and 0 <= cy < spec.y_size):
            problems.append(f"{label} {(cx, cy)} lies outside the {spec.x_size}x{spec.y_size} grid")
        elif grid[cy][cx] == BLOCKED:
            problems.append(f"{label} cell {(cx, cy)} is blocked (value F)")
    problems.extend(maze_failures(grid, spec))
    seen = reachable(grid, spec)
    total = sum(grid[y][x] != BLOCKED for y in range(spec.y_size) for x in range(spec.x_size))
    if spec.exit not in seen:
        problems.append("EXIT is not reachable from ENTRY")
    if len(seen) != total:
        problems.append(f"maze is not fully connected ({len(seen)}/{total} passable cells reachable)")
    if spec.perfect:
        open_sides = sum(
            grid[y][x] != BLOCKED and not has_wall(grid[y][x], side)
            for y in range(spec.y_size)
            for x in range(spec.x_size)
            for _, _, side, _ in _DIRS
        )
        passages = open_sides // 2
        if passages != total - 1:
            problems.append(f"PERFECT=True but maze is not a tree ({passages} passages for {total} cells)")
    return problems


def evaluate(case: Case, outcomes: list[RunOutcome]) -> CaseResult:
    """Turn raw run outcomes into a pass/fail verdict with reasons."""
    problems: list[str] = []
    first = outcomes[0]
    if first.returncode is None:
        return CaseResult(case, (f"timed out after {TIMEOUT_S:.0f}s (possible infinite loop)",), first)
    if "Traceback" in first.stderr:
        problems.append("crashed with an uncaught Python traceback")
    if case.expect_success:
        problems.extend(success_problems(case, first))
    elif first.maze_text is not None:
        problems.append("wrote an output file for an invalid config")
    elif first.returncode == 0 and not ERROR_MESSAGE_RE.search(f"{first.stdout}\n{first.stderr}"):
        problems.append("accepted an invalid config (exit code 0 and no clear error message)")
    match case.twice:
        case None:
            pass
        case "stable":
            if outcomes[1].maze_text is not None and first.maze_text != outcomes[1].maze_text:
                problems.append("same SEED produced two different mazes")
        case "varies":
            if first.maze_text is not None and first.maze_text == outcomes[1].maze_text:
                problems.append("SEED=None produced two identical mazes")
        case unreachable:
            assert_never(unreachable)
    return CaseResult(case, tuple(problems), first)


def execute(main_py: Path, case: Case) -> CaseResult:
    """Run the case in an isolated temp directory (twice for seed checks)."""
    with tempfile.TemporaryDirectory(prefix="maze_test_") as tmp:
        workdir = Path(tmp)
        outcomes = [run_program(main_py, case, workdir)]
        if case.twice is not None:
            second = workdir / "second"
            second.mkdir()
            outcomes.append(run_program(main_py, case, second))
    return evaluate(case, outcomes)


def build_cases() -> list[Case]:
    """The full scenario table: valid shapes first, then invalid inputs."""

    def valid(
        name: str,
        note: str = "",
        twice: Literal["stable", "varies"] | None = None,
        **overrides: str,
    ) -> Case:
        config = dict(BASE_CONFIG)
        config.update(overrides)
        return Case(name, config, True, twice=twice, note=note)

    def invalid(name: str, note: str = "", **overrides: str) -> Case:
        config = dict(BASE_CONFIG)
        config.update(overrides)
        return Case(name, config, False, note=note)

    def missing(key: str) -> Case:
        config = dict(BASE_CONFIG)
        del config[key]
        return Case(f"missing key {key}", config, False)

    cases = [
        # --- valid configs -------------------------------------------------
        valid("baseline (the provided config.txt)"),
        valid("perfect maze", PERFECT="True", SEED="7"),
        valid("small 5x5", HEIGHT="5", WIDTH="5", ENTRY="0,0", EXIT="4,4"),
        valid("minimal 2x2", HEIGHT="2", WIDTH="2", ENTRY="0,0", EXIT="1,1"),
        valid("single-row corridor", HEIGHT="8", WIDTH="1", ENTRY="0,0", EXIT="7,0"),
        valid("single-column corridor", HEIGHT="1", WIDTH="8", ENTRY="0,0", EXIT="0,7"),
        valid("tall 30 rows", HEIGHT="4", WIDTH="30", ENTRY="0,0", EXIT="3,29"),
        valid("wide 30 columns", HEIGHT="30", WIDTH="4", ENTRY="0,0", EXIT="29,3"),
        valid("entry/exit in opposite corners", ENTRY="0,0", EXIT="19,14"),
        valid("large 150x150", HEIGHT="150", WIDTH="150", ENTRY="0,0", EXIT="149,149"),
        valid("fixed seed is reproducible", twice="stable", SEED="12345"),
        valid("SEED=None varies between runs", twice="varies"),
        Case(
            "comments and blank lines are ignored",
            dict(BASE_CONFIG),
            True,
            raw=(
                "# a comment\n"
                "\n"
                "HEIGHT=6\n"
                "WIDTH=9\n"
                "ENTRY=0,0\n"
                "EXIT=5,8\n"
                "OUTPUT_FILE=maze.txt\n"
                "PERFECT=True\n"
                "SEED=3\n"
            ),
        ),
        # --- invalid configs: must fail cleanly, never crash ---------------
        Case("config file does not exist", None, False),
        Case("empty config file", dict(BASE_CONFIG), False, raw=""),
        missing("HEIGHT"),
        missing("WIDTH"),
        missing("ENTRY"),
        missing("EXIT"),
        missing("OUTPUT_FILE"),
        missing("PERFECT"),
        invalid("HEIGHT=0", HEIGHT="0"),
        invalid("HEIGHT negative", HEIGHT="-3"),
        invalid("HEIGHT not a number", HEIGHT="abc"),
        invalid("HEIGHT not an integer", HEIGHT="3.5"),
        invalid("WIDTH=0", WIDTH="0"),
        invalid("WIDTH not a number", WIDTH="abc"),
        invalid("ENTRY x out of bounds", ENTRY="20,0"),
        invalid("ENTRY y out of bounds", ENTRY="0,15"),
        invalid("ENTRY negative coordinate", ENTRY="-1,0"),
        invalid("EXIT out of bounds", EXIT="9,99"),
        invalid("ENTRY not a pair", ENTRY="5"),
        invalid("ENTRY non-numeric", ENTRY="a,b"),
        invalid(
            "ENTRY equals EXIT",
            note="flip this to a valid case if your spec allows entry == exit",
            ENTRY="5,5",
            EXIT="5,5",
        ),
        invalid("PERFECT not a boolean", PERFECT="maybe"),
        invalid("OUTPUT_FILE empty", OUTPUT_FILE=""),
        Case(
            "line without '=' separator",
            dict(BASE_CONFIG),
            False,
            raw=render_config(dict(BASE_CONFIG)).replace("HEIGHT=20", "HEIGHT 20"),
        ),
    ]
    return cases


def _paint(text: str, code: str, enabled: bool) -> str:
    return f"\033[{code}m{text}\033[0m" if enabled else text


def _print_stream_excerpt(label: str, text: str) -> None:
    """Print useful parts of a captured stream without dumping huge mazes."""
    lines = text.rstrip().splitlines()
    if len(lines) > 20:
        omitted = len(lines) - 16
        lines = lines[:8] + [f"... {omitted} lines omitted ..."] + lines[-8:]
    for line in lines:
        print(f"       {label}| {line}")


def report(results: list[CaseResult], verbose: bool) -> int:
    """Print per-case feedback and the summary; return the process exit code."""
    color = sys.stdout.isatty()
    failed = 0
    for result in results:
        if not result.problems:
            print(_paint(f"[PASS] {result.case.name}", "32", color))
            continue
        failed += 1
        print(_paint(f"[FAIL] {result.case.name}", "31;1", color))
        for problem in result.problems:
            print(f"       - {problem}")
        if result.case.note:
            print(f"       note: {result.case.note}")
        if verbose:
            _print_stream_excerpt("stdout", result.first.stdout)
            _print_stream_excerpt("stderr", result.first.stderr)
    total = len(results)
    print("─" * 60)
    print(_paint(f"{total} cases · {total - failed} passed · {failed} failed", "31;1" if failed else "32;1", color))
    if failed and not verbose:
        print("rerun with --verbose to see the program's stdout/stderr on failures")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    verbose = "--verbose" in argv or "-v" in argv
    positional = [arg for arg in argv[1:] if not arg.startswith("-")]
    main_py = Path(positional[0] if positional else os.environ.get("MAZE_MAIN", "a_maze_ing.py")).resolve()
    if not main_py.is_file():
        print(f"error: maze program not found: {main_py}", file=sys.stderr)
        print("usage: python3 maze_tester.py [path/to/a_maze_ing.py] [--verbose]", file=sys.stderr)
        return 2
    print(f"Testing {main_py}\n")
    results = [execute(main_py, case) for case in build_cases()]
    return report(results, verbose)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
