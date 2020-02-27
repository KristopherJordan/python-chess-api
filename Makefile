
install:
	pip install -r requirements.txt

test:
	@printf "Starting tests \n"
	pytest tests/test_*.py
	@printf "\n Finished tests \n"

build:
	@printf "Creating image"
	docker image build -f Dockerfile -t "chess" .

start-worker:
	@printf "Starting worker  \n"
	python worker.py

start:
	@printf "Start services"
	docker-compose -f docker-compose.yml up -d --remove-orphans

stop:
	@printf "Stopping service"
	docker-compose -f docker-compose.yml stop

logs:
	docker-compose -f docker-compose.yml logs -f --tail=30
