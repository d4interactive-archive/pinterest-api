.PHONY: test clean virtualenv bootstrap

test:
	sh -c '. _virtualenv/bin/activate;  nosetests pin_py/tests/pinterest_api_tests.py'

	
bootstrap: virtualenv
ifneq ($(wildcard Requirements),)
	_virtualenv/bin/pip install -r Requirements
endif
	make clean
	make test

virtualenv:
	virtualenv _virtualenv
	_virtualenv/bin/pip install --upgrade pip
	_virtualenv/bin/pip install --upgrade setuptools