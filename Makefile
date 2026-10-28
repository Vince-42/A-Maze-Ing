SYSTEM_PYTHON = python3
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python

install:
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install flake8 mypy

run:
	$(VENV_PYTHON) a_maze_ing.py config.txt

debug:
	$(VENV_PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	find . -path "./.venv" -prune -o -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -path "./.venv" -prune -o -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -path "./.venv" -prune -o -type d -name ".pytest_cache" -prune -exec rm -rf {} +

lint:
	$(VENV_PYTHON) -m flake8 . --exclude=.venv
	$(VENV_PYTHON) -m mypy . --exclude '(^|/)\.venv/' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint