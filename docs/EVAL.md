# Evaluation

## Metrics

We evaluate the Coach Agent on two primary dimensions:

1.  **Actionability**: Does the recommendation propose a concrete, physical action?
2.  **Groundedness**: Is the recommendation supported by the data (e.g., citing specific metrics)?

## Running Evaluation

Use the `verify_brain.py` script (or `saricoach.eval.eval_runner`) to run the evaluation harness against a set of scenarios defined in `saricoach/eval/scenarios_eval.jsonl`.

```bash
python verify_brain.py
```

## Scenarios

Scenarios cover various store states:
- High stockout risk
- Low visibility for high-margin brands
- High demand opportunities
