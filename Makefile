.PHONY: test clean virtualenv bootstrap

test:
	sh -c '. _virtualenvv/bin/activate;  nosetests pin_py/tests/pinterest_api_tests.py'

	
bootstrap: virtualenv
ifneq ($(wildcard Requirements),)
	_virtualenvv/bin/pip install -r Requirements
endif
	make clean
	make test

virtualenv:
	virtualenv _virtualenvv
	_virtualenvv/bin/pip install --upgrade pip
	_virtualenvv/bin/pip install --upgrade setuptools