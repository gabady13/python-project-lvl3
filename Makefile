install:
	@poetry install

build:
	@poetry build

package-install:
	pip install --user dist/*.whl

package-uninstall:
	pip uninstall hexlet-code

make lint:
	poetry run flake8 hexlet-code
