fmt:
	poetry run ruff format src tests

lint:
	poetry run ruff check src tests
	poetry run mypy src

test:
	poetry run pytest tests
