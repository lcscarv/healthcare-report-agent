.PHONY: build up build-up down logs run feed-database run-report generate-report create-test-data run-tests create-data-run-tests

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f app

run:
	docker-compose run app

build-up-run: build up run


feed-database:
	python -m app.data.data_manager

run-report:
	streamlit run streamlit_app.py

generate-report: feed-database run-report

create-test-data:
	python -m app.data.create_test_data

run-tests:
	pytest tests/ 

create-data-run-tests: create-test-data run-tests