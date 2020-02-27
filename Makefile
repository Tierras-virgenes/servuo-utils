SHELL := /bin/bash

PROJECT=servuo-utils
export ROOTDIR:=$(shell pwd)

uninstall:
	pip uninstall -y ${PROJECT} || true

develop: uninstall
	pip install --editable .

clean: clean-build clean-pyc clean-dist

clean-build:
	rm -fr build/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-dist:
	rm -fr dist/

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

dist-build:
	python setup.py bdist_wheel

dist-check:
	twine check dist/*

dist-upload:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*