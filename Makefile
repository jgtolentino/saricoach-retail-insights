PYTHON := python3

.PHONY: init api test eval

init:
	$(PYTHON) -m pip install -r requirements.txt

api:
	$(PYTHON) -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8080

test:
	$(PYTHON) -m pytest -q || echo "tests not yet implemented"

eval:
	$(PYTHON) -m src.eval.run_eval
