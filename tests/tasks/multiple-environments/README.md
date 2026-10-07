# multiple-environments

Tester deploy av en task-environment som er avhengig av en annen environment.

Alle avhengigheter må være installert ved deploy

https://www.union.ai/docs/v2/union/user-guide/tasks/task-configuration/multiple-environments/

- `task/main.py` definerer entrypoint-tasken. Den kaller `numpy_task` fra `modules/numpy_task`.
- Hver environment har sin egen image-definisjon. `pyproject.toml` inneholder gruppene `pytest-task` og `numpy-task`.
- CI deployer begge environmentene til dev og prod: [workflow](../../../.github/workflows/deploy-test-multiple-environments.yaml).