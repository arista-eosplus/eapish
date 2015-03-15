#!/usr/bin/make
# WARN: gmake syntax
########################################################
# Makefile for eapish
#
# useful targets:
#	make sdist -- build python source distribution
#	make pep8 -- pep8 checks
#	make pyflakes -- pyflakes checks
#	make check -- manifest checks
#	make tests -- run all of the tests
#	make clean -- clean distutils
#
########################################################
# variable section

NAME = "eapish"

PYTHON=python
COVERAGE=coverage
SITELIB = $(shell $(PYTHON) -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

VERSION := $(shell cat VERSION)

########################################################

all: clean pep8 pyflakes tests check

pep8:
	-pep8 -r --ignore=E501,E221,W291,W391,E302,E251,E203,W293,E231,E303,E201,E225,E261,E241 eapish/ test/

pyflakes:
	pyflakes eapish/ test/

check:
	check-manifest

clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
	rm -rf MANIFEST
	rm -rf *.egg-info
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete

sdist: clean
	$(PYTHON) setup.py sdist

tests:
	$(COVERAGE) run -m unittest discover test/unit -v

