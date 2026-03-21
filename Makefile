.PHONY: dev test lint typecheck security build docker-build docker-up clean

dev:
	uvicorn api_toolkit:create_app --factory --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --cov=api_toolkit --cov-report=term-missing --cov-report=xml

lint:
	ruff check . --fix && ruff format .

typecheck:
	mypy api_toolkit/ --ignore-missing-imports

security:
	bandit -r api_toolkit/ -ll && pip-audit

build:
	python -m build

docker-build:
	docker build -t python-api-toolkit:latest .

docker-up:
	docker compose up --build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf dist/ build/ .pytest_cache/ .mypy_cache/ coverage.xml
