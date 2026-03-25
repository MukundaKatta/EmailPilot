.PHONY: install test lint format check clean

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/
	mypy src/emailpilot/

format:
	black src/ tests/
	ruff check --fix src/ tests/

check: lint test

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
