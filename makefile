ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env

endif


build:
	docker compose up --build -d --remove-orphans

up:	
	docker compose up -d

down:
	docker compose down

show-logs:
	docker compose logs


migrate:
	docker compose exec api python manage.py migrate

makemigrations:
	docker compose exec api python manage.py makemigrations

show-urls:
	docker compose exec api python manage.py show_urls

check:
	docker compose exec api python manage.py check

migrate_elasticsearch:
	docker compose exec api python manage.py search_index --rebuild

createsuperuser:
	docker compose exec api python manage.py createsuperuser

collectstatic:
	docker compose exec api python manage.py collectstatic --no-input --clear

django-check:
	docker compose exec api python manage.py check

init_db:
	docker compose exec api python manage.py db_init 30

shell:	
	docker compose exec api python manage.py shell_plus

down-v:
	docker compose down -v 

volume:
	docker volume inspect rentals-app_postgres_data


rental-db:
	docker compose exec postgres-db psql --username=mubakusystemsadmin --dbname=rentals

generate-api-schema:
	docker compose exec api python manage.py spectacular --file schema.yaml

generate-api-schema-json:
	docker compose exec api python manage.py spectacular --file schema.json

test:
	docker compose exec api pytest -p no:warnings --cov=.

test-html:
	docker compose exec api pytest -p no:warnings --cov=. --cov-report html

flake8:
	docker compose exec api flake8

black-check:
	docker compose exec api black --check --exclude=migrations .

black-diff:
	docker compose exec api black --diff --exclude=migrations .

black:
	docker compose exec api black --exclude=migrations .

isort-check:
	docker compose exec api isort . --check-only --skip env --skip migrations

isort-diff:
	docker compose exec api isort . --diff --skip env --skip  migrations
	
isort:
	docker compose exec api isort . --skip env --skip migrations

lint: 
	flake8 black-check isort-check

config:
	docker compose config

watch:
	docker compose exec api watchmedo shell-command --patterns="*.py" --recursive --command='make lint test' .


