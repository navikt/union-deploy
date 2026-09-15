# Deploy Union/Flyte tasks with GitHub Actions

Use this reusable workflow to deploy the Flyte tasks defined in a Python file to Union from your repository's CI pipeline.

## Prerequisites

Before deploying:

- Your GitHub repository must be registered with the Union project you want to deploy to. Contact the dataplattform team if it is not registered or you are unsure.
- Your dependency file must include `flyte`.
- Your task must be defined in a Python (`.py`) file.

## Deploy from CI

Create a workflow such as `.github/workflows/deploy.yaml` in the repository containing your task:

```yaml
name: Deploy Union task

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  deploy:
    permissions:
      contents: read
      id-token: write
    uses: navikt/union-deploy/.github/workflows/deploy.yaml@v1
    with:
      flyte-task-file: ./tasks/my_task.py
      dependency-file: ./pyproject.toml
      union-project: my-union-project
      union-domain: development
```

Adjust the file paths, project, domain, and trigger for your repository. A deploy runs all Flyte entities found in `flyte-task-file`.

The permissions are required so the workflow can check out your repository and authenticate to the platform without long-lived credentials.

## Inputs

| Input | Required | Description |
| --- | --- | --- |
| `flyte-task-file` | Yes | Path to the Python file containing the Flyte task or tasks, for example `./tasks/my_task.py`. |
| `dependency-file` | Yes | Path to `pyproject.toml` or a `requirements*.txt` file, for example `./requirements.txt`. Dependencies are installed from its directory. |
| `union-project` | Yes | Union project registered for this GitHub repository. Only letters, numbers, and hyphens are accepted. |
| `union-domain` | Yes | Target domain: `development`, `staging`, or `production`. |
| `python-version` | No | Python version to use with a requirements file, for example `3.12`. With `pyproject.toml`, configure Python in the project instead. |

The workflow installs your project dependencies so it can import the task definition and run the Flyte deployment command. This does not build the task image in GitHub Actions: Union builds the deployable image using its remote image builder.

To select Python when using a requirements file:

```yaml
    with:
      flyte-task-file: ./tasks/my_task.py
      dependency-file: ./requirements.txt
      union-project: my-union-project
      union-domain: development
      python-version: "3.12"
```

## Troubleshooting

- **Authentication or permission failure:** Verify that the GitHub repository is registered with the value passed to `union-project`, and that both permissions from the example are present.
- **`flyte` is not installed:** Add `flyte` to your `pyproject.toml` or requirements file.
- **Task or dependency file does not exist:** Paths are relative to the repository root. Check the spelling and location of both files.
- **Invalid domain:** Use exactly `development`, `staging`, or `production`.
- **Dependencies differ from your local environment:** The workflow currently does not respect `uv.lock`. When using `pyproject.toml`, it resolves dependencies again through our internal PyPI proxy. This can select versions that differ from your local lockfile. This is subject to change in the future when a new PyPI proxy (Artifact Keeper) is ready, at that time we will require `uv.lock` files to be built with that proxy.
