.PHONY: devc help write server test shell worker redis-dev

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  server	- Start the application server"
	@echo "  shell	- Start the Django shell"
	@echo "  redis-dev	- Start the Redis server"
	@echo "  worker	- Start the Celery worker"
	@echo "  write	- Start the documentation server"
	@echo "  devc	- Build the client dev server"
	@echo "  test	- Run the test suite"
	@echo "  help	- Display this help message"

devc:
	@echo "Starting client dev server..."
	@cd client && bun dev

write:
	@echo "Starting docusaurus server..."
	@cd doc && bun start

server:
	@echo "Starting application server..."
	@python ./manage.py runserver

test:
	@echo "Running test suite..."
	@python ./manage.py test --keepdb -v 2

shell:
	@echo "Starting shell..."
	@python ./manage.py shell

worker:
	@echo "Starting Celery worker..."
	@celery -A server worker -l INFO

redis-dev:
	@echo "Starting Redis server..."
	@docker run -d -p 6379:6379 --name redis-music redis:alpine
