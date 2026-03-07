VENV = venv/bin
PYTHON = python3
SOURCES = maze_generator

install:
	$(PYTHON) -m venv venv
	$(VENV)/pip install --upgrade pip
	$(VENV)/pip install -r requirements.txt

run:
	$(VENV)/$(PYTHON) -m $(SOURCES).a_maze_ing config.txt

debug:
	$(VENV)/$(PYTHON) -m pdb $(SOURCES)/a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	$(VENV)/flake8 .
	$(VENV)/mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	$(VENV)/flake8 .
	$(VENV)/mypy --strict .

test:
	@clear
	$(VENV)/$(PYTHON) -m $(SOURCES).a_maze_ing test/test_config.txt

.PHONY: test install run debug clean lint lint-strict