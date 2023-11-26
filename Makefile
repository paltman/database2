start:
	python manage.py runserver
requirements:
	set -e ;\
	pip-compile --upgrade --output-file=requirements.txt requirements.in ;\
	pip-compile --upgrade --output-file=requirements-dev.txt requirements-dev.in ;\
	pip install -r requirements-dev.txt
lint:
	set -e ;\
	ruff check database2 --fix
	ruff check dataentry --fix
