# pyproject-dependency-file

Tester hvordan `pyproject.toml` kan oppgi avhengighetene til en Flyte-task.

- `main.py` definerer tasken og bruker `Image.with_uv_project(...)` til å installere avhengighetene i imaget.
- `pyproject.toml` oppgir Python-avhengighetene.
- CI deployer eksempelet til dev og prod: [workflow](../../../.github/workflows/deploy-test-pyproject-dependency-file.yaml).