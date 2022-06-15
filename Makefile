install:
	@poetry install

build:
	@poetry build

package-install:build
	python3 -m pip install dist/*.whl

package-uninstall:
	pip uninstall hexlet-code

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest
