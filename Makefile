.PHONY: clean clean-pyc clean-build  \
	install install-dev install-test install-docs \
	lint flake8 isort \
	tests test-unit test-integration docs publish

# all: clean lint test docs

IGNORE_VENV ?= FALSE

PACKAGE_FOLDERS = convex_sdk tools tests

FLAKE8_PARAMETERS = --max-line-length=132 --statistics $(PACKAGE_FOLDERS)

ISORT_PARAMETERS = --use-parentheses  --ignore-whitespace --check-only --multi-line=3 --force-grid-wrap=2 --line-width=132 --diff $(PACKAGE_FOLDERS)

PIP_CMD=pip3

clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

install: virtualvenv
	$(PIP_CMD) install -e ".[dev]" -e ".[test]" -e ".[docs]"

install-dev: virtualvenv
	$(PIP_CMD) install -e ".[dev]"

install-test: virtualvenv
	$(PIP_CMD) install -e ".[test]"

install-docs: virtualvenv
	$(PIP_CMD) install -e ".[docs]"


virtualvenv:
ifeq ($(IGNORE_VENV),FALSE)
ifeq ($(VIRTUAL_ENV),)
		@echo "you are about to install this module when you are not in a virtual environment"
		exit 1
endif
endif


lint: flake8 isort

flake8:
	flake8 $(FLAKE8_PARAMETERS)

isort:
	isort $(ISORT_PARAMETERS)

tests:
	pytest tests

test-unit:
	pytest tests/unit

test-integration:
	pytest tests/integration

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(MAKE) -C docs man

publish:
	make clean
	pip install twine
	python3 setup.py sdist bdist_wheel
	echo "__token__" | python3 -m twine upload dist/*
