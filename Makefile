# Check linting errors in API code
test-pylint-api:
	@pylint src/api/tools
	@pylint src/api/app.py
	@pylint src/api/settings.py

# Check linting errors in Detector code
test-pylint-detector:
	@pylint src/detector/tools
	@pylint src/detector/app.py
	@pylint src/detector/settings.py

# Run unit tests for api service
test-api-units:
	@pytest src/api/tests/

# Run unit tests for detector service
test-detector-units:
	@pytest src/detector/tests/

# Check app linting errors
test-pylint: test-pylint-api test-pylint-detector

# Run app unit tests
test-units: test-api-units test-detector-units

# Rebuild application
build:
	@docker-compose build

# Run application locally with two celery workers
start:
	@docker-compose up --scale celery-worker=2

# Stop application
stop:
	@docker-compose down

# Clear all docker containers & images
clear:
	@docker rmi $(docker images -a -q) -f
	@docker rm $(docker ps -a -q) -f

