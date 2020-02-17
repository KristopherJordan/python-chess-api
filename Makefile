
start:
	@printf "Starting worker  \n"
	python worker.py

install:
	pip install -r requirements.txt

test:
	@printf "Starting tests \n"
	pytest tests/test_*.py
	@printf "\n Finished tests \n"
