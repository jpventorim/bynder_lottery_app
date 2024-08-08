DOCKER=docker-compose exec -it lottery
MANAGE_PY = python manage.py

# 
# Build and Setup
# 
build:
	docker-compose pull
	docker-compose up --build

docker-migrate:
	$(DOCKER) $(MANAGE_PY) migrate

docker-down:
	docker-compose down -v --remove-orphans ${ARGS}

# 
# Runners
# 
docker-run:
	docker-compose up ${ARGS}

# 
# Debugging/Testing
# 
django-shell:
	$(DOCKER) $(MANAGE_PY) shell

docker-shell:
	$(DOCKER) /bin/bash

test:
	$(DOCKER) pytest -v -xs .

# 
# Linters
# 
mypy-check:
	$(DOCKER) poetry run mypy

ruff-format:
	$(DOCKER) poetry run ruff format .

ruff-fix:
	$(DOCKER) poetry run ruff check --fix .

lint:
	make mypy-check
	make ruff-fix