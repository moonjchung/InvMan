# AGENTS

## Development Guidelines

- Run `poetry run ruff check .`, `poetry run mypy`, and `poetry run pytest` before committing.
- Honor the 88-character line length and the existing exclusions defined in `pyproject.toml`.
- If tests require a database, ensure any necessary setup or migrations are run before executing them.
