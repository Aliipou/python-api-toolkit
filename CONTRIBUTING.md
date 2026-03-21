# Contributing to python-api-toolkit

Thanks for your interest in contributing!

## How to contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Make your changes with tests
4. Run the test suite (`pytest tests/`)
5. Submit a pull request

## Code style

- Use `ruff` for linting
- Use `black` for formatting
- All public functions need docstrings
- Type hints are required

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: fix a bug
docs: update documentation
test: add or fix tests
refactor: refactor code without behavior change
```

## Running tests

```bash
pip install -e ".[dev]"
pytest tests/ -v --cov=api_toolkit
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
