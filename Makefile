VENV = venv/bin

install:
	$(VENV)/pip install -r requirements.txt 

run:
	$(VENV)/python3 a_maze_ing.py config.txt 

debug:
	$(VENV)/python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	$(VENV)/flake8 .
	$(VENV)/mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	$(VENV)/flake8 .
	$(VENV)/mypy --strict .