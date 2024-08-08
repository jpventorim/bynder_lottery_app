DOCKER=docker compose exec -it lottery
MANAGE_PY = python manage.py

# 
# Build and Setup
# 
build:
	docker compose pull
	docker compose up --build

docker-migrate:
	$(DOCKER) $(MANAGE_PY) migrate

docker-down:
	docker compose down -v --remove-orphans ${ARGS}

docker-run:
	docker compose up ${ARGS}

create-test-user:
	curl -X 'POST' \
		'http://localhost:8000/users/register' \
		-H 'accept: */*' \
		-H 'Content-Type: application/json' \
		-d '{"email": "test_user@example.com", "password": "pass", "first_name": "Test", "last_name": "User"}'

get-token-test-user:
	curl -X 'POST' \
	'http://localhost:8000/token/pair' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"password": "pass","email": "test_user@example.com"}'

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