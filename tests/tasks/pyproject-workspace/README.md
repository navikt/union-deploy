# pyproject-workspace

Tester deploy av en task fra et medlem i et uv-workspace.

- CI kjører fra `packages/task` og bruker medlemmets `pyproject.toml`, ikke fila i roten av workspacet.
- Medlemmets `pyproject.toml` oppgir Flyte som avhengighet. Tasken bruker et ferdigbygd image, så testen krever ikke at den eksterne image-byggeren pakker workspacet.
- CI deployer eksempelet til dev og prod: [workflow](../../../.github/workflows/deploy-test-pyproject-workspace.yaml).
