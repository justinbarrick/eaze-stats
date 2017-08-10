.PHONY: build
build:
	pip install -r requirements.txt

.PHONY: run
run:
	python eaze.py

.PHONY: test
test:
	nosetests -v -s
