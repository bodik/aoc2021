all:

venv:
	apt-get install pyton3-virtualenv
	python3 -m venv venv

install-deps:
	pip install flake8
	pip install pylint

lint:
	python3 -m flake8 part2.py
	python3 -m pylint part2.py

# make day day=dayX
day:
	mkdir $(day)
	ln -s ../Makefile $(day)/Makefile
	ln -s ../.flake8 $(day)/.flake8
	ln -s ../.pylintrc $(day)/.pylintrc
