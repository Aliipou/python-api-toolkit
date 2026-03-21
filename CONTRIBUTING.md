# Contributing to python-api-toolkit

Thank you for your interest! Here is how to contribute.

## Setup

```bash
git clone https://github.com/Aliipou/python-api-toolkit.git
cd python-api-toolkit
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Workflow

1. Fork the repo and create a feature branch
2. Write your code and tests
3. Run `make lint && make test` — both must pass
4. Open a pull request with a clear description

## Code Style

- Python 3.11+
- `ruff` for linting and formatting
- Type hints required on all public functions
- Docstrings for all public classes and methods

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` tests only
- `chore:` tooling/config

## Running Tests

```bash
make test
```

## License

By contributing you agree your code is licensed under MIT.
