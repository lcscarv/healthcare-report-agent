.PHONY: feed-database run-report generate-report create-test-data run-tests create-data-run-tests

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