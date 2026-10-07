# pyproject-groups

Tester installasjon av valgte PEP 735-avhengighetsgrupper fra `pyproject.toml`.

- `pytest_task.py` velger gruppen `pytest-task`. `numpy_pytest_task.py` velger både `pytest-task` og `numpy-task`.
- `pyproject.toml` definerer gruppene. Image-definisjonene bruker `.with_uv_project(..., extra_args="--group ...")`. Det første eksempelet legger også til en `loaded_modules`-code bundle.
- CI deployer begge eksemplene til dev og prod: [workflow](../../../.github/workflows/deploy-test-pyproject-groups.yaml).