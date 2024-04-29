# LazySplit

![](https://github.com/linkstaple/SQR-project-S24/actions/workflows/deploy.yml/badge.svg)

![](https://raw.githubusercontent.com/linkstaple/SQR-project-S24/_xml_coverage_reports/data/main/badge.svg)
![](https://raw.githubusercontent.com/linkstaple/SQR-project-S24/_badges/data/flake8_badge.svg)
![](https://raw.githubusercontent.com/linkstaple/SQR-project-S24/_badges/data/cyclomatic_complexity.svg)
![](https://raw.githubusercontent.com/linkstaple/SQR-project-S24/_badges/data/bandit_badge.svg)

## Coverage report

<!-- BEGIN REPORT -->
Package | Line Rate | Branch Rate | Health
-------- | --------- | ----------- | ------
src | 100% | 100% | ✔
src.api | 93% | 100% | ✔
src.config | 95% | 75% | ✔
src.db | 94% | 82% | ✔
src.middleware | 88% | 100% | ✔
src.model | 100% | 100% | ✔
src.service | 90% | 74% | ✔
src.static | 80% | 100% | ✔
src.tests.integration | 98% | 100% | ✔
src.tests.service | 100% | 100% | ✔
**Summary** | **95%** (555 / 583) | **89%** (118 / 132) | ✔
<!-- END REPORT -->

## Mutation testing report
<!-- BEGIN MUTATION REPORT -->
Total mutations | Passed | Failed | Rate
----------------|--------|--------|------
5 | 5 | 0 | 100%
<!-- END MUTATION REPORT -->

## Install dependencies
`poetry install`

## Run project
`poetry run python src/main.py`
