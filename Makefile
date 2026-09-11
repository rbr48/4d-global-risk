.PHONY: lint format test check all

# ============================================================================
# 4D-MGRFF Development Makefile
# ============================================================================

# Run flake8 static analysis
lint:
	python -m flake8 models/ src/ tests/ --max-line-length 120 --ignore E501,W503

# Run black code formatter (check mode - no changes)
format-check:
	python -m black --check --line-length 120 models/ src/ tests/

# Run black code formatter (apply changes)
format:
	python -m black --line-length 120 models/ src/ tests/

# Run full test suite
test:
	python -m pytest tests/ -v

# Run all checks (lint + format check + tests)
check: lint format-check test

# Default target
all: check
