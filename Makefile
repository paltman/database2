start:
	docker compose up -d
build:
	docker compose build
rebuild:
	docker compose down && docker volume rm database2_db && docker compose build && docker compose up -d
migrate:
	docker exec -it database2-django python manage.py migrate
migrations:
	docker exec -it database2-django python manage.py makemigrations
shell:
	docker exec -it database2-django python manage.py shell
requirements:
	set -e ;\
	pip-compile --upgrade --output-file=requirements.txt requirements.in ;\
	pip-compile --upgrade --output-file=requirements-dev.txt requirements-dev.in ;\
	pip install -r requirements-dev.txt
lint:
	set -e ;\
	ruff check database2 --fix
db:
	docker exec -it database2-postgres psql -U database2 database2
