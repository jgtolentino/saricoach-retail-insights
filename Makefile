.PHONY: test-unit test-api test-e2e test-all run-backend run-dashboard

test-unit:
	python3 -m pytest tests -q

test-api:
	# API tests are now part of the main test suite in tests/
	@echo "Running all tests..."
	python3 -m pytest tests -q

test-e2e:
	npx playwright test

test-all: test-unit test-api
	# e2e can be optional in CI or run manually

run-backend:
	uvicorn service.app.main:app --reload --port 8000

run-dashboard:
	cd dashboard && npm run dev
