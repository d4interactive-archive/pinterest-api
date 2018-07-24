.PHONY: test clean virtualenv bootstrap

test:
	sh -c '. _virtualenv/bin/activate;  nosetests tests.pinterest_api_tests:MyTestCase.test_working'

	
bootstrap: virtualenv
ifneq ($(wildcard requirements),) 
	_virtualenv/bin/pip install -r Requirements
endif
	make clean
	make test

virtualenv:
	virtualenv _virtualenv
	_virtualenv/bin/pip install --upgrade pip
	_virtualenv/bin/pip install --upgrade setuptools