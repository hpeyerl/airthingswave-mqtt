# 
# Herb is lazy and can't remember how to do stuff.
#
PYTHON:=python3
PKG:=airthings-mqtt
#
# can't handle the import so force the version.  XXX(hp).
#
#VERSION:=${shell ${PYTHON} src/${PKG}/__init__.py}
VERSION=0.1

all: clean build test

clean:
	rm -rf dist build /tmp/pip-* src/airthings-mqtt.egg-info
	rm -rf venv /home/hpeyerl/.cache/pip/wheels/8e/22/27/96436ab8e9371fdad01caa13fb9fb0a0e80299ad8ea6b24312
	rm -fr /tmp/venv

build:
	${PYTHON} setup.py sdist bdist_wheel

#
# Test a local install
#
test:
	virtualenv -p ${PYTHON} venv
	venv/bin/pip -v install dist/${PKG}-${VERSION}.tar.gz
	find venv -name "*${PKG}*"

#
# Test an install from pypi test server
#
testpypi:
	cd /tmp ; \
	virtualenv -p ${PYTHON} venv && \
	venv/bin/pip install -i https://testpypi.python.org/pypi ${PKG} && \
	find venv -name "*${PKG}*"
		
upload_test:
	twine upload -r test dist/${PKG}-${VERSION}*

upload_real:
	twine upload -r pypi dist/${PKG}-${VERSION}*

show.%: 
	@echo $*=$($*)
