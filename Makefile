.PHONY: help install shell server migrate makemigrations superuser collectstatic test clean runserver createsuperuser check

help:
	@echo "Available commands:"
	@echo "  install        - Install dependencies using pipenv"
	@echo "  shell          - Start Django shell"
	@echo "  server         - Run development server"
	@echo "  migrate        - Apply database migrations"
	@echo "  makemigrations - Create new migrations"
	@echo "  superuser      - Create superuser"
	@echo "  collectstatic  - Collect static files"
	@echo "  test           - Run tests"
	@echo "  clean          - Clean Python cache files"
	@echo "  check          - Check for Django issues"

install:
	python3 -m pipenv install

shell:
	python3 -m pipenv run python manage.py shell

server:
	python3 -m pipenv run python manage.py runserver

runserver: server

migrate:
	python3 -m pipenv run python manage.py migrate

makemigrations:
	python3 -m pipenv run python manage.py makemigrations

superuser:
	python3 -m pipenv run python manage.py createsuperuser

createsuperuser: superuser

collectstatic:
	python3 -m pipenv run python manage.py collectstatic --noinput

test:
	python3 -m pipenv run python manage.py test

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyo" -delete

check:
	python3 -m pipenv run python manage.py check