make install:
	poetry install
	poetry run pre-commit install

make test:
	poetry run pytest

make lint:
	poetry run pre-commit run --all-files

make run:
	poetry run streamlit run greencompute_frontend/app.py

make build:
	docker build -t greencompute-frontend .
