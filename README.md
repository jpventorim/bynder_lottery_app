# Bynder Lottery System

## Introduction

This django project implements a simple but extendable Lottery System. Users can register themselves with username and password and obtain an API token (JWT) with those credentials. The access token can be used to make API calls to submit ballots for the lottery dates within the week. An user can also check the results of past lotteries.

Every day at midnight, a task runs to select a winning ballot from all the ballots submitted for the day before. If this task fails for some reason, it will automatically retry every minute up to 10 times.


## Tech Stack

The project is built using **Django** as web framework, **Django-Ninja** for serialization and schema validation, **Celery** and **Redis** to manage scheduled tasks and **Postgres** for the database.


### Setup

To run this project you will need to have [Python 3.12](https://www.python.org/downloads/) and [Docker](https://www.docker.com/) installed in your computer:


1. `make build`: Pull, build and run Docker container

1. `make docker-migrate`: Apply Django database migrations


### API Utilization

The API can be tested on the browser on [localhost:8000/docs](localhost:8000/docs). The commands below can speed up the process.

1. `make create-test-user`: Creates a test user with credentials: 
   - username: "test_user"
   - password: "pass"

1. `make get-token-test-user`: Uses above test user to generate tokens.
   - `access`: Used as Bearer token for Authenticated API calls
   - `refresh`: Used to refresh the token on `/token/refresh` endpoint



### Testing the Task
Since the task is scheduled to run at midnight, to easily test, we can instead create a schedule to run every minute.

- Stop the container
- On `lottery_app/settings.py`, look for `CELERY_BEAT_SCHEDULE` at the end of the file and uncomment the block of code so the task runs every minute.
- `make docker-run` to run the container again. 

The task called `lottery_draw_every_minute` should show up in the logs now.

### Useful Commands

- Run container without re-building:
  ```shell
  make docker-run
  ```

- Run tests and fail on first error:
  ```shell
  make test
  ```

- Put the container down and clean up the database:
  ```shell
  make docker-down
  ```
- Access container terminal:
  ```shell
  make docker-shell
  ```

- Access django shell:
  ```shell
  make django-shell
  ```

- Run linter, formatter and type checkers:
  ```shell
  make lint
  ```

## Author

- **João Paulo Ventorim**

