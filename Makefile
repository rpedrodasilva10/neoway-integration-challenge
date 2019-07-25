start: 
	#commands necessary to start the API
	python run.py
check: 
	#include command to test the code and show the results
	# to ignore deprecated warnings
	pytest -W ignore

setup: 
	#if needed to setup the enviroment before starting it
	pip install -r requirements.txt


run: 
	# Checks the dependencies, the test and run the api
	make setup
	make check
	make start

