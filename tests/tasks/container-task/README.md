# container-task

Tester deploy av en Flyte-task som kjører en egen `ContainerTask`.

- `main.py` definerer en container-task basert på Alpine og en Python-task som kjører den.
- `pyproject.toml` oppgir avhengighetene som trengs for å laste tasken.
- CI deployer eksempelet til dev og prod: [workflow](../../../.github/workflows/deploy-test-container-task.yaml).