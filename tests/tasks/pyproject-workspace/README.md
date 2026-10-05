# Workspace member fixture

The deploy workflow runs from `packages/task` and receives the member's
`pyproject.toml`, not the workspace root's. Without an explicit environment path,
uv creates `.venv` at the workspace root, so looking beside the member's
`pyproject.toml` fails.

Flyte is declared only in the member to verify that its dependencies are installed.
The task uses a prebuilt image so this fixture tests the deployment environment
without requiring the remote builder to package a uv workspace.
