# requirements-dependency-file

Tester bruk av `requirements.txt` for å oppgi avhengighetene til en Flyte-task.

- `main.py` bruker `Image.with_requirements(...)` til å installere avhengighetene i imaget.
- `requirements.txt` oppgir pakkene som trengs for å laste tasken.
- CI deployer eksempelet til dev og prod: [workflow](../../../.github/workflows/deploy-test-requirements-dependency-file.yaml).
