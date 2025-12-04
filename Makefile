.PHONY: build up down logs run feed-database run-report generate-report create-test-data run-tests create-data-run-tests

# Build the Docker image
build:
	docker-compose build

# Start the Docker containers
up:
	docker-compose up -d

# Stop the Docker containers
down:
	docker-compose down

# View logs from the app container
logs:
	docker-compose logs -f app

run:
	docker-compose run app

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